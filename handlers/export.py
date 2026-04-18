import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv
import io
from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from database.db import get_all_expenses_csv, get_user_language
from utils.translations import t

router = Router()


@router.message(Command("export"))
async def export_handler(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    rows = get_all_expenses_csv(user_id)

    if not rows:
        await message.answer(t(lang, "no_expenses", label="all time"))
        return

    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Amount ($)", "Category", "Note"])
    for row in rows:
        writer.writerow([row["date"], f"{row['amount']:.2f}", row["category"], row["note"] or ""])

    csv_bytes = output.getvalue().encode("utf-8-sig")  # utf-8-sig for Excel compatibility

    await message.answer_document(
        BufferedInputFile(csv_bytes, filename="expenses.csv"),
        caption=t(lang, "export_caption", count=len(rows))
    )
