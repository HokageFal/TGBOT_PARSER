import os
from pathlib import Path
from aiogram import types, Router, F, Bot
from parser_bot.database.core import get_db
from parser_bot.database.crud import add_skills
from parser_bot.services.read_file import read_pdf, read_docx, read_doc
from parser_bot.services.regex import extract_section, individual_word
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

os.makedirs("downloads", exist_ok=True)

@router.message(F.document)
async def download_file(message: types.Message, bot: Bot):
    async for session in get_db():
        try:
            await message.delete()
        except:
            pass

        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_name = message.document.file_name

        save_path = Path("downloads") / file_name

        await bot.download_file(
            file.file_path,
            str(save_path))
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

        skills = await add_skills(session=session, telegram_id=message.from_user.id, skills=words, username=message.from_user.username)
        builder = InlineKeyboardBuilder()
        for i in skills:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"skill_{i}"))
        builder.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_start"))
        builder.adjust(3)
        await message.answer(f"Ваши навыки успешно загружены.",
                            reply_markup=builder.as_markup())