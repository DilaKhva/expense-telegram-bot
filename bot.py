import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_TOKEN
from database.models import init_db
from handlers.ai_handler import router as ai_router
from handlers.export import router as export_router
from handlers.manage import router as manage_router

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(export_router)
dp.include_router(manage_router)
dp.include_router(ai_router)


async def main():
    init_db()
    print("✅ Bot is working!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
