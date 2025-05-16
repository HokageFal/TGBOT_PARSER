import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from parser_bot.config import BOT_TOKEN
import asyncio
from bot.handlers.commands import router

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
