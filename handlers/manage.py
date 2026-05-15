import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import calendar

from database.db import (
    get_recent_expenses, delete_expense, update_expense,
    get_expense_by_id, get_user_language, get_expenses,
    get_expense_years, get_expense_months
)
from utils.translations import t

router = Router()

MONTH_NAMES = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}


class EditState(StatesGroup):
    waiting_for_edit = State()


def _format_date(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if d.day == 1:
            return d.strftime("%B %Y")
        return d.strftime("%b %d, %Y")
    except:
        return date_str


def _build_manage_keyboard(expenses, lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for row in expenses:
        label = f"{_format_date(row['date'])} — ${row['amount']:.2f} [{row['category']}]"
        buttons.append([
            InlineKeyboardButton(text=label, callback_data=f"noop_{row['id']}"),
        ])
        buttons.append([
            InlineKeyboardButton(text=t(lang, "delete_btn"), callback_data=f"del_{row['id']}"),
            InlineKeyboardButton(text=t(lang, "edit_btn"), callback_data=f"edit_{row['id']}"),
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _build_year_keyboard(years: list) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for year in years:
        row.append(InlineKeyboardButton(text=year, callback_data=f"manage_year_{year}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _build_month_keyboard(year: str, months: list) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for month in months:
        row.append(InlineKeyboardButton(
            text=MONTH_NAMES.get(month, month),
            callback_data=f"manage_month_{year}_{month}"
        ))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    # Back button
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="manage_back_years")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def show_manage_list(message: Message, lang: str, user_id: int = None, date_from: str = None, date_to: str = None):
    if user_id is None:
        user_id = message.from_user.id

    # Get available years
    years = get_expense_years(user_id)

    if not years:
        await message.answer(t(lang, "no_expenses", label="all time"), parse_mode="Markdown")
        return

    # If only one year, skip year selection
    if len(years) == 1:
        months = get_expense_months(user_id, years[0])
        if len(months) == 1:
            # Only one month — show directly
            date_from = f"{years[0]}-{months[0]}-01"
            last_day = calendar.monthrange(int(years[0]), int(months[0]))[1]
            date_to = f"{years[0]}-{months[0]}-{last_day:02d}"
            rows = list(get_expenses(user_id=user_id, date_from=date_from, date_to=date_to))
            if not rows:
                await message.answer(t(lang, "no_expenses", label="all time"), parse_mode="Markdown")
                return
            keyboard = _build_manage_keyboard(rows, lang)
            await message.answer(t(lang, "manage_title"), reply_markup=keyboard, parse_mode="Markdown")
        else:
            await message.answer(
                f"📅 *{years[0]}* — which month?",
                reply_markup=_build_month_keyboard(years[0], months),
                parse_mode="Markdown"
            )
    else:
        await message.answer(
            "📅 *Which year?*",
            reply_markup=_build_year_keyboard(years),
            parse_mode="Markdown"
        )


# Year selection callback
@router.callback_query(lambda c: c.data.startswith("manage_year_"))
async def manage_year_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    year = callback.data.replace("manage_year_", "")
    months = get_expense_months(user_id, year)

    await callback.message.edit_text(
        f"📅 *{year}* — which month?",
        reply_markup=_build_month_keyboard(year, months),
        parse_mode="Markdown"
    )
    await callback.answer()


# Back to years
@router.callback_query(lambda c: c.data == "manage_back_years")
async def manage_back_years_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    years = get_expense_years(user_id)
    await callback.message.edit_text(
        "📅 *Which year?*",
        reply_markup=_build_year_keyboard(years),
        parse_mode="Markdown"
    )
    await callback.answer()


# Month selection callback
@router.callback_query(lambda c: c.data.startswith("manage_month_"))
async def manage_month_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    parts = callback.data.replace("manage_month_", "").split("_")
    year, month = parts[0], parts[1]

    date_from = f"{year}-{month}-01"
    last_day = calendar.monthrange(int(year), int(month))[1]
    date_to = f"{year}-{month}-{last_day:02d}"

    rows = list(get_expenses(user_id=user_id, date_from=date_from, date_to=date_to))

    if not rows:
        await callback.message.edit_text(
            t(lang, "no_expenses", label=f"{MONTH_NAMES.get(month, month)} {year}"),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    keyboard = _build_manage_keyboard(rows, lang)
    month_name = MONTH_NAMES.get(month, month)
    await callback.message.edit_text(
        f"📋 *{month_name} {year} expenses — tap to manage:*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()


# Delete callback
@router.callback_query(lambda c: c.data.startswith("del_"))
async def delete_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    expense_id = int(callback.data.split("_")[1])
    delete_expense(expense_id, user_id)
    await callback.message.edit_text(t(lang, "deleted"))
    await callback.answer()


# Edit callback
@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    expense_id = int(callback.data.split("_")[1])

    row = get_expense_by_id(expense_id, user_id)
    if not row:
        await callback.answer(t(lang, "expense_not_found"))
        return

    await state.set_state(EditState.waiting_for_edit)
    await state.update_data(expense_id=expense_id)

    await callback.message.answer(
        f"📝 Current:\n"
        f"📅 {_format_date(row['date'])}  💰 ${row['amount']:.2f}  📂 {row['category']}  📝 {row['note'] or '—'}\n\n"
        + t(lang, "edit_prompt"),
        parse_mode="Markdown"
    )
    await callback.answer()


# Process edit input
@router.message(EditState.waiting_for_edit)
async def process_edit(message: Message, state: FSMContext):
    from services.ai_service import analyze_message, _parse_amount
    import re
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    data = await state.get_data()
    expense_id = data.get("expense_id")

    text = message.text.lower().strip()
    edit_data = {}

    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    if numbers and any(w in text for w in ["amount", "summa", "price", "cost", "but", "not", "change", "to"]):
        edit_data["amount"] = _parse_amount(numbers[-1])
    elif numbers and len(text.split()) <= 3:
        edit_data["amount"] = _parse_amount(numbers[0])
    else:
        result = await analyze_message(message.text, lang=lang)
        edit_data = result.get("data", {})

    update_expense(
        expense_id=expense_id,
        user_id=user_id,
        amount=edit_data.get("amount"),
        category=edit_data.get("category"),
        note=edit_data.get("note"),
        date=edit_data.get("date")
    )

    row = get_expense_by_id(expense_id, user_id)
    await state.clear()

    if row:
        await message.answer(
            t(lang, "edit_saved",
              date=_format_date(row["date"]),
              amount=f"{row['amount']:.2f}",
              category=row["category"],
              note=row["note"] or "—"),
            parse_mode="Markdown"
        )
    else:
        await message.answer(t(lang, "expense_not_found"))
