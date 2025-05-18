import logging
from datetime import datetime
from idlelib.editor import keynames
import os
from aiogram.filters.command import Command
from aiogram import types, Router, F, Bot
from pyexpat.errors import messages

from parser_bot.config import aclient
from parser_bot.database.core import get_db
from parser_bot.database.crud import get_user, add_skills, get_skills, delete_skill
from parser_bot.services.read_file import read_pdf, read_docx, read_doc
from parser_bot.services.regex import extract_section, individual_word
from pathlib import Path
from aiogram.utils.keyboard import InlineKeyboardBuilder
os.makedirs("downloads", exist_ok=True)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    async for session in get_db():
        user = await get_user(session,
                              telegram_id=message.from_user.id,
                              username=message.from_user.username)
        kb = [
            [types.KeyboardButton(text="Загрузить свое резюме")],
            [types.KeyboardButton(text="Мои навыки")],
            [types.KeyboardButton(text="О проекте")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Приветствую вас! {user.username}", reply_markup=keyboard)

@router.message(F.text == "Загрузить свое резюме")
async def resume_add(message: types.Message):
    await message.answer("Скинь свое резюме")

@router.message(F.document)
async def download_file(message: types.Message, bot: Bot):
    async for session in get_db():

        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_name = message.document.file_name

        save_path = Path("downloads") / file_name

        await bot.download_file(
            file.file_path,
            str(save_path)
        )
        ext = save_path.suffix.lower()

        read_file = ""
        if ext == ".pdf":
            read_file = read_pdf(str(save_path))
        elif ext == ".docx":
            read_file = read_docx(str(save_path))
        elif ext == ".doc":
            read_file = read_doc(str(save_path))
        else:
            await message.answer("Данный формат файла пока не поддерживается, используйте pdf, docx или doc.")
            raise ValueError("Формат не поддерживается")

        extract = extract_section(read_file)
        words = individual_word(extract)

        skills = await add_skills(session=session, telegram_id=message.from_user.id, skills=words)
        builder = InlineKeyboardBuilder()
        for i in skills:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"skill_{i}"))
        builder.adjust(3)
        await message.answer(f"Ваши навыки успешно загружены.",
                             reply_markup=builder.as_markup())

@router.message(F.text=="Мои навыки")
async def my_skills(message: types.Message):
    async for session in get_db():
        builder = InlineKeyboardBuilder()
        skills = await get_skills(session, message.from_user.id)
        if not skills:
            await message.answer("У вас нет навыков, отправьте свое резюме в чат")

        for i in skills:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"skill_{i}"))
        builder.adjust(3)
        await message.answer(f"Ваши навыки", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("skill_"))
async def get_one_skill(callback: types.CallbackQuery):
    skill_name = callback.data.replace("skill_", "")

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Удалить",
                                           callback_data=f"delete_skill_{skill_name}"))
    builder.add(types.InlineKeyboardButton(text="Вопросы",
                                           callback_data=f"question_skill_{skill_name}"))

    await callback.message.answer(f"Навык {skill_name}", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("delete_skill_"))
async def delete_skills(callback: types.CallbackQuery):
    async for session in get_db():
        skill_name = callback.data.replace("delete_skill_", "")
        await delete_skill(session, callback.from_user.id, skill_name)
        await callback.message.answer(f"Навык успешно удален")

# @router.message()
# async def openai_message(message: types.Message):
#     try:
#         response = await aclient.chat.completions.create(
#             model = "gpt-4o-mini",
#             messages = [
#                 {"role": "user", "content": message.text}
#             ]
#         )
#         await message.answer(response.message.content)
#     except Exception as e:
#         await message.answer(f"Ошибка: {e}")