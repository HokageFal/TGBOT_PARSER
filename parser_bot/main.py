import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from parser_bot.config import BOT_TOKEN
import asyncio
from bot.handlers import routers
from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

for router in routers:
    dp.include_router(router)

async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запустить бота'),
    ]

    await bot.set_my_commands(main_menu_commands)

dp.startup.register(set_main_menu)

async def main():
    await dp.start_polling(bot)

# 1. Починить инлайн кнопки при старте
# 2. Сделать возвращение на пагинацию при добавлении в колецию

if __name__ == "__main__":
    asyncio.run(main())