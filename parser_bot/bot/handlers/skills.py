from aiogram import types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser_bot.database.core import get_db
from parser_bot.database.crud import get_skills, add_skill, delete_skill, add_skills

router = Router()

@router.message(F.text == "Мои навыки")
@router.callback_query(F.data == "my_skills")
async def my_skills(request: types.Message | types.CallbackQuery):
    if isinstance(request, types.CallbackQuery):
        message = request.message
    else:
        message = request


    async for session in get_db():
        try:
            await message.delete()
        except:
            pass

        builder = InlineKeyboardBuilder()
        skills = await get_skills(session, message.from_user.id)
        if not skills:
            await message.answer("У вас нет навыков, отправьте свое резюме в чат")

        for i in skills:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"skill_{i}"))

        builder.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_start"))
        builder.adjust(3)

        await message.answer(f"Ваши навыки", reply_markup=builder.as_markup())
#
# @router.message(F.text & ~F.text.in_("Добавить навыки в ручную"))
# async def add_manual_skill(message: types.Message):
#     async for session in get_db():
#         try:
#             await message.delete()
#         except:
#             pass
#
#         skill = message.text.strip()
#         await add_skill(session=session, telegram_id=message.from_user.id, title=skill)
#
#         builder = InlineKeyboardBuilder()
#         builder.add(types.InlineKeyboardButton(
#             text="Мои навыки",
#             callback_data="back_to_skills"
#         ))
#         builder.add(types.InlineKeyboardButton(
#             text="Назад",
#             callback_data="back_to_start"
#         ))
#
#         if skill is None:
#             await message.answer(f"Навык '{skill}' уже есть в вашем списке навыков",
#                               reply_markup=builder.as_markup())
#
#         await message.answer(
#             f"Навык '{skill}' успешно добавлен!",
#             reply_markup=builder.as_markup()
#         )

@router.callback_query(F.data.startswith("delete_skill_"))
async def delete_skills(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    async for session in get_db():
        skill_name = callback.data.replace("delete_skill_", "")
        await delete_skill(session, callback.from_user.id, skill_name)
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_start"
        ))

        await callback.message.answer(f"Навык успешно удален", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("skill_"))
async def get_one_skill(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    skill_name = callback.data.replace("skill_", "")

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Удалить",
                                        callback_data=f"delete_skill_{skill_name}"))
    builder.add(types.InlineKeyboardButton(text="Вопросы",
                                        callback_data=f"question_skill_{skill_name}"))
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_skills"))

    await callback.message.answer(f"Навык {skill_name}", reply_markup=builder.as_markup())

@router.callback_query(F.data == "back_to_skills")
async def back_to_skills(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    async for session in get_db():
        builder = InlineKeyboardBuilder()
        skills = await get_skills(session, callback.from_user.id)

        if not skills:
            await callback.message.answer("У вас нет навыков, отправьте свое резюме в чат")

        for i in skills:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"skill_{i}"))
        builder.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_start"))
        builder.adjust(3)

        await callback.message.answer(f"Ваши навыки", reply_markup=builder.as_markup())
