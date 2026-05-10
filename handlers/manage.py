import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from database.db import (
    get_recent_expenses, delete_expense, update_expense,
    get_expense_by_id, get_user_language
)
from utils.translations import t

router = Router()


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


async def show_manage_list(message: Message, lang: str, user_id: int = None):
    if user_id is None:
        user_id = message.from_user.id
    rows = get_recent_expenses(user_id, limit=10)

    if not rows:
        await message.answer(t(lang, "no_expenses", label="all time"))
        return

    keyboard = _build_manage_keyboard(rows, lang)
    await message.answer(t(lang, "manage_title"), reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("del_"))
async def delete_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    expense_id = int(callback.data.split("_")[1])

    delete_expense(expense_id, user_id)
    await callback.message.edit_text(t(lang, "deleted"))
    await callback.answer()


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
        + t(lang, "edit_prompt")
    )
    await callback.answer()


@router.message(EditState.waiting_for_edit)
async def process_edit(message: Message, state: FSMContext):
    from services.ai_service import analyze_message
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    data = await state.get_data()
    expense_id = data.get("expense_id")

    # Use AI to parse what user wants to change
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
        await message.answer(t(lang, "edit_saved",
            date=_format_date(row["date"]),
            amount=f"{row['amount']:.2f}",
            category=row["category"],
            note=row["note"] or "—"
        ))
    else:
        await message.answer(t(lang, "expense_not_found"))
