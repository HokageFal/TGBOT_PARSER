from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser_bot.database.core import get_db
from parser_bot.database.crud import get_question_for_skills
import logging
logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data.startswith("question_skill_"))
async def get_question(callback: types.CallbackQuery):
    try:
        async for session in get_db():
            try:
                await callback.message.delete()
            except:
                pass

            skill_name = callback.data.replace("question_skill_", "")
            logger.info(f"Processing skill: {skill_name}")
            questions = await get_question_for_skills(session, skill_name)

            builder = InlineKeyboardBuilder()

            builder.add(types.InlineKeyboardButton(text="Назад к навыкам", callback_data="back_to_skills"))
            builder.adjust(3)

            if not questions:
                await callback.message.answer("Для этого навыка пока нет вопросов", reply_markup=builder.as_markup())
                return

            for question in questions:
                await callback.message.answer(f"{question.text}", reply_markup=builder.as_markup())
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")