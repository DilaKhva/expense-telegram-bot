import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from aiogram import Bot, Dispatcher

from config import TELEGRAM_TOKEN
from database.models import init_db
from handlers.ai_handler import router

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    init_db()
    print("✅ Bot is working!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
