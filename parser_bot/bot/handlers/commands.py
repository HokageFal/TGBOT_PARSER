import logging
from aiogram.filters.command import Command
from aiogram import types, Router


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")