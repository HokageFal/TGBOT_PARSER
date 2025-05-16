import logging
from idlelib.editor import keynames
import os
from aiogram.filters.command import Command
from aiogram import types, Router, F, Bot

from parser_bot.services.read_file import read_pdf, read_docx
from parser_bot.services.regex import extract_section

os.makedirs("downloads", exist_ok=True)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Загрузить свое резюме")],
        [types.KeyboardButton(text="О проекте")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Приветствую вас!", reply_markup=keyboard)

@router.message(F.text == "Загрузить свое резюме")
async def resume_add(message: types.Message):
    await message.answer("Скинь свое резюме")

@router.message(F.document)
async def download_file(message: types.Message, bot: Bot):
    try:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_name = message.document.file_name

        await bot.download_file(
            file.file_path,
            f"downloads/{file_name}"
        )
        if file_name.endswith(".pdf"):
            read_pdw = print(read_pdf(f"downloads/{file_name}"))
        if file_name.endswith((".docx", ".doc")):
            read_doc = print(read_docx(f"downloads/{file_name}"))
            extract = extract_section(read_doc, "Навыки", "Резюме обновлено")
            print(extract)
        await message.answer(f"Резюме {file_name} успешно загружено!")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")