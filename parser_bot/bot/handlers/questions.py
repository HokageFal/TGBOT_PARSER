from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser_bot.database.core import get_db
from parser_bot.database.crud import get_question_for_skills, get_question_for_skill_pagination, get_total_items, \
    get_total_question
# import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
# logger = logging.getLogger(__name__)

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
            # logger.info(f"Processing skill: {skill_name}")
            question = await get_question_for_skill_pagination(session, skill_name, page=1)
            total_items = await get_total_question(session, skill_name)


            builder = InlineKeyboardBuilder()

            buttons = []
            if total_items:
                buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next1_{skill_name}_2"))

            if buttons:
                builder.row(*buttons)

            builder.row(types.InlineKeyboardButton(
                text="Наза",
                callback_data="back_to_skills"
            ))

            if not question:
                await callback.message.answer("Для этого навыка пока нет вопросов",
                                              reply_markup=builder.as_markup())
                return

            await callback.message.answer(f"{question[0].text}, Всего вопросов {total_items}",
                                          reply_markup=builder.as_markup())
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")


@router.callback_query(F.data.startswith(("prev1_", "next1_")))
async def handle_pagination(callback: types.CallbackQuery):
    async for session in get_db():
        try:
            await callback.message.delete()
        except:
            pass

        parts = callback.data.split("_")
        action = parts[0]
        skill_name = parts[1]
        current_page = int(parts[2])

        if action == "prev":
            new_page = max(1, current_page)
        else:
            new_page = current_page

        # logger.info(f"Processing skill: {skill_name}")
        question = await get_question_for_skill_pagination(session, skill_name, page=new_page)
        total_items = await get_total_question(session, skill_name)


        if new_page > total_items:
            await callback.answer("Это последняя страница!")
            await session.commit()
            return

        builder = InlineKeyboardBuilder()

        buttons = []
        if new_page > 1:
            buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"prev1_{skill_name}_{new_page - 1}"))

        if new_page < total_items:
            buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next1_{skill_name}_{new_page + 1}"))

        if buttons:
            builder.row(*buttons)

        builder.row(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_skills"
        ))

        if not question:
            await callback.message.answer("Для этого навыка пока нет вопросов",
                                          reply_markup=builder.as_markup())
            return

        await callback.message.answer(f"{question[0].text}",
                                      reply_markup=builder.as_markup())

