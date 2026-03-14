import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from services.ai_service import analyze_message
from database.db import add_expense, get_expenses, get_stats, clear_expenses
from utils.charts import generate_pie_chart


def _format_date(date_str: str) -> str:
    """If day is 01, show as Month YYYY, otherwise show full date"""
    try:
        from datetime import datetime
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if d.day == 1:
            return d.strftime("%B %Y")
        return d.strftime("%Y-%m-%d")
    except:
        return date_str


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Hey! I'm your AI expense tracker.\n\n"
        "Just talk to me naturally, for example:\n\n"
        "💬 \"spent 12 on lunch\"\n"
        "💬 \"paid 3.50 for coffee today\"\n"
        "💬 \"what did I spend this week?\"\n"
        "💬 \"show me this month's stats\"\n\n"
        "💵 Please use USD ($) for all amounts.\n\n"
        "⚠️ Send one expense at a time — I process one message per request!\n\n"
        "🗑 Use /clear to delete all your data."
    )


@router.message(Command("clear"))
async def clear_handler(message: Message):
    clear_expenses(user_id=message.from_user.id)
    await message.answer("🗑 All your expenses have been deleted. Fresh start! ✨")


@router.message()
async def ai_message_handler(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    # Detect multiple lines
    lines = [l.strip() for l in user_text.strip().splitlines() if l.strip()]
    if len(lines) > 1:
        await message.answer(
            "⚠️ Looks like you sent multiple things at once!\n\n"
            "Please send *one expense per message*, like:\n"
            "💬 \"spent 12 on lunch\"\n"
            "💬 \"paid 3.50 for coffee\"\n\n"
            "I'll track each one separately! 😊",
            parse_mode="Markdown"
        )
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    result = await analyze_message(user_text)

    intent = result.get("intent")
    data = result.get("data", {})
    ai_reply = result.get("reply", "")

    if intent == "add_expense":
        amount = data.get("amount")
        category = data.get("category") or "Other"
        note = data.get("note") or ""
        date = data.get("date") or None

        if amount and amount > 0:
            add_expense(
                user_id=user_id,
                amount=float(amount),
                category=category,
                note=note,
                date=date
            )
            display_date = _format_date(date) if date else "Today"
            await message.answer(
                f"✅ Saved!\n\n"
                f"📅 Date: {display_date}\n"
                f"💰 Amount: ${float(amount):,.2f}\n"
                f"📂 Category: {category}\n"
                f"📝 Note: {note or '—'}"
            )
        else:
            await message.answer(
                "❌ Couldn't detect the amount.\n\n"
                "💵 Please use USD. For example:\n"
                "\"spent 50 on lunch\""
            )

    elif intent == "list_expenses":
        period = data.get("period") or "month"
        rows = get_expenses(user_id=user_id, period=period)
        period_text = {"today": "Today", "week": "This week", "month": "This month", "year": "This year", "all": "All time"}.get(period, "This month")

        if not rows:
            await message.answer(f"📭 No expenses found for {period_text.lower()}.")
            return

        total = sum(row["amount"] for row in rows)
        lines = [f"📋 *{period_text}'s expenses:*\n"]
        for row in rows:
            date_str = _format_date(row["date"])
            lines.append(f"• {date_str} — ${row['amount']:,.2f} [{row['category']}] {row['note'] or ''}")
        lines.append(f"\n💰 *Total: ${total:,.2f}*")
        await message.answer("\n".join(lines), parse_mode="Markdown")

    elif intent == "get_stats":
        period = data.get("period") or "month"
        rows = get_stats(user_id=user_id, period=period)
        period_text = {"today": "Today", "week": "This week", "month": "This month", "year": "This year", "all": "All time"}.get(period, "This month")

        if not rows:
            await message.answer(f"📭 No stats available for {period_text.lower()}.")
            return

        total = sum(row["total"] for row in rows)
        lines = [f"📊 *{period_text}'s stats:*\n"]
        for row in rows:
            percent = (row["total"] / total) * 100
            lines.append(f"• {row['category']}: ${row['total']:,.2f} ({percent:.0f}%)")
        lines.append(f"\n💰 *Total: ${total:,.2f}*")
        await message.answer("\n".join(lines), parse_mode="Markdown")

    elif intent == "get_chart":
        period = data.get("period") or "month"
        rows = get_stats(user_id=user_id, period=period)
        period_text = {"today": "Today", "week": "This week", "month": "This month", "year": "This year", "all": "All time"}.get(period, "This month")

        if not rows:
            await message.answer(f"📭 No data to chart for {period_text.lower()}.")
            return

        chart = generate_pie_chart(rows, period_text)
        await message.answer_photo(
            BufferedInputFile(chart.read(), filename="chart.png"),
            caption=f"📊 {period_text}'s spending breakdown"
        )

    else:
        await message.answer(ai_reply)
