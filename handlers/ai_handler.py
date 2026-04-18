import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Router
from aiogram.types import Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from datetime import datetime

from services.ai_service import analyze_message
from database.db import add_expense, get_expenses, get_stats, clear_expenses, get_user_language, set_user_language, get_all_expenses_csv
from handlers.manage import show_manage_list
from services.budget import get_budget_advice
from utils.charts import generate_pie_chart
from utils.translations import t


def _format_date(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if d.day == 1:
            return d.strftime("%B %Y")
        return d.strftime("%b %d, %Y")
    except:
        return date_str


def _period_label(date_from: str, date_to: str) -> str:
    if not date_from and not date_to:
        return "All time"
    if date_from == date_to:
        return _format_date(date_from)
    if date_from and date_to:
        return f"{_format_date(date_from)} – {_format_date(date_to)}"
    if date_from:
        return f"From {_format_date(date_from)}"
    return f"Until {_format_date(date_to)}"


def _lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
        ]
    ])


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(t(lang, "start"), parse_mode="Markdown")


@router.message(Command("language"))
async def language_handler(message: Message):
    lang = get_user_language(message.from_user.id)
    await message.answer(t(lang, "choose_language"), reply_markup=_lang_keyboard())


@router.callback_query(lambda c: c.data in ["lang_en", "lang_uz"])
async def language_callback(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    set_user_language(callback.from_user.id, lang)
    await callback.message.edit_text(t(lang, "language_set"))
    await callback.answer()
    # Show updated start message
    await callback.message.answer(t(lang, "start"))


@router.message(Command("clear"))
async def clear_handler(message: Message):
    lang = get_user_language(message.from_user.id)
    clear_expenses(user_id=message.from_user.id)
    await message.answer(t(lang, "cleared"))


@router.message()
async def ai_message_handler(message: Message):
    user_id = message.from_user.id
    user_text = message.text
    lang = get_user_language(user_id)

    # Detect multiple lines
    lines = [l.strip() for l in user_text.strip().splitlines() if l.strip()]
    if len(lines) > 1:
        await message.answer(t(lang, "multi_line"), parse_mode="Markdown")
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    result = await analyze_message(user_text, lang=lang)

    intent = result.get("intent")
    data = result.get("data", {})
    ai_reply = result.get("reply", "")

    if intent == "add_expense":
        amount = data.get("amount")
        category = data.get("category") or "Other"
        note = data.get("note") or ""
        date = data.get("date") or None

        if amount and amount > 0:
            add_expense(user_id=user_id, amount=float(amount), category=category, note=note, date=date)
            display_date = _format_date(date) if date else "Today"
            await message.answer(t(lang, "saved",
                date=display_date,
                amount=f"{float(amount):,.2f}",
                category=category,
                note=note or "—"
            ))
        else:
            await message.answer(t(lang, "no_amount"))

    elif intent == "list_expenses":
        date_from = data.get("date_from") or None
        date_to = data.get("date_to") or None
        rows = get_expenses(user_id=user_id, date_from=date_from, date_to=date_to)
        label = _period_label(date_from, date_to)

        if not rows:
            await message.answer(t(lang, "no_expenses", label=label))
            return

        total = sum(row["amount"] for row in rows)
        lines = [t(lang, "expenses_header", label=label)]
        for row in rows:
            lines.append(f"• {_format_date(row['date'])} — ${row['amount']:,.2f} [{row['category']}] {row['note'] or ''}")
        lines.append(t(lang, "expenses_total", total=f"{total:,.2f}"))
        await message.answer("\n".join(lines), parse_mode="Markdown")

    elif intent == "get_stats":
        date_from = data.get("date_from") or None
        date_to = data.get("date_to") or None
        rows = get_stats(user_id=user_id, date_from=date_from, date_to=date_to)
        label = _period_label(date_from, date_to)

        if not rows:
            await message.answer(t(lang, "no_stats", label=label))
            return

        total = sum(row["total"] for row in rows)
        lines = [t(lang, "stats_header", label=label)]
        for row in rows:
            percent = (row["total"] / total) * 100
            lines.append(f"• {row['category']}: ${row['total']:,.2f} ({percent:.0f}%)")
        lines.append(t(lang, "expenses_total", total=f"{total:,.2f}"))
        await message.answer("\n".join(lines), parse_mode="Markdown")

    elif intent == "get_chart":
        date_from = data.get("date_from") or None
        date_to = data.get("date_to") or None
        rows = get_stats(user_id=user_id, date_from=date_from, date_to=date_to)
        label = _period_label(date_from, date_to)

        if not rows:
            await message.answer(t(lang, "no_chart", label=label))
            return

        chart = generate_pie_chart(rows, label)
        await message.answer_photo(
            BufferedInputFile(chart.read(), filename="chart.png"),
            caption=t(lang, "chart_caption", label=label)
        )

    elif intent == "budget_advice":
        await message.bot.send_chat_action(message.chat.id, "typing")
        advice = await get_budget_advice(user_id=user_id, lang=lang)
        await message.answer(advice)

    elif intent == "manage":
        await show_manage_list(message, lang)

    elif intent == "export":
        import csv, io
        rows = get_all_expenses_csv(user_id)
        if not rows:
            await message.answer(t(lang, "no_expenses", label="all time"))
            return
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Amount ($)", "Category", "Note"])
        for row in rows:
            writer.writerow([row["date"], f"{row['amount']:.2f}", row["category"], row["note"] or ""])
        csv_bytes = output.getvalue().encode("utf-8-sig")
        await message.answer_document(
            BufferedInputFile(csv_bytes, filename="expenses.csv"),
            caption=t(lang, "export_caption", count=len(rows))
        )

    else:
        await message.answer(ai_reply)
