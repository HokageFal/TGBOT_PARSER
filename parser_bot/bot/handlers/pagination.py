from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from parser_bot.database.core import get_db
from aiogram import Router, F, types

from parser_bot.database.crud import get_skill_pagination, get_total_items, add_skill

router = Router()

@router.callback_query(F.data == "add_skills_manual")
async def ask_for_skill_for_inline(callback: types.CallbackQuery):
    async for session in get_db():
        try:
            await callback.message.delete()
        except:
            pass

        items = await get_skill_pagination(session=session, page=1, user_id=callback.from_user.id)
        total_items = await get_total_items(session=session, user_id=callback.from_user.id)
        total_pages = max(1, (total_items + 4) // 5)
        builder = InlineKeyboardBuilder()

        for i in items:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"add_skill_{i}"))

        buttons = []
        if total_pages > 1:
            buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_2"))

        if buttons:
            builder.row(*buttons)

        builder.row(types.InlineKeyboardButton(
            text="Отмена",
            callback_data="back_to_start"
        ))

        await callback.message.answer(
            f"Выберите навык из выделенных чтобы добавить в список твоих навыков:\n Страница 1/{total_pages}",
            reply_markup=builder.as_markup()
        )

@router.message(F.text == "Добавить навыки в ручную")
async def ask_for_skill(message: types.Message):
    async for session in get_db():
        try:
            await message.delete()
        except:
            pass

        items = await get_skill_pagination(session=session, user_id=message.from_user.id, page=1)
        total_items = await get_total_items(session=session, user_id=message.from_user.id)
        total_pages = max(1, (total_items + 4) // 5)
        builder = InlineKeyboardBuilder()

        for i in items:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"add_skill_{i}"))

        buttons = []
        if total_pages > 1:
            buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_2"))

        if buttons:
            builder.row(*buttons)

        builder.row(types.InlineKeyboardButton(
            text="Отмена",
            callback_data="back_to_start"
        ))

        await message.answer(
            f"Выберите навык из выделенных чтобы добавить в список твоих навыков:\n Страница 1/{total_pages}",
            reply_markup=builder.as_markup()
        )


@router.callback_query(F.data.startswith(("prev_", "next_")))
async def handle_pagination(callback: types.CallbackQuery):
    async for session in get_db():
        try:
            await callback.message.delete()
        except:
            pass

        action, page = callback.data.split("_")
        current_page = int(page)

        if action == "prev":
            new_page = max(1, current_page)
        else:
            new_page = current_page

        items = await get_skill_pagination(session=session, page=new_page, user_id=callback.from_user.id)
        total_items = await get_total_items(session=session,  user_id=callback.from_user.id)
        total_pages = max(1, (total_items + 4) // 5)

        if new_page > total_pages:
            await callback.answer("Это последняя страница!")
            await session.commit()
            return

        builder = InlineKeyboardBuilder()
        for i in items:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"add_skill_{i}"))

        buttons = []
        if new_page > 1:
            buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"prev_{new_page - 1}"))

        if new_page < total_pages:
            buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_{new_page + 1}"))

        if buttons:
            builder.row(*buttons)

        builder.row(types.InlineKeyboardButton(
            text="Отмена",
            callback_data="back_to_start"
        ))

        await callback.message.answer(
            text=f"Выберите навык из выделенных чтобы добавить в список твоих навыков:\n Страница {new_page}/{total_pages}",
            reply_markup=builder.as_markup()
        )

@router.callback_query(F.data.startswith("add_skill_"))
async def add_to_db_user(callback: types.CallbackQuery):
    async for session in get_db():
        try:
            await callback.message.delete()
        except:
            pass

        skill_name = callback.data.replace("add_skill_", "")
        print(skill_name)
        await add_skill(session=session,
                         telegram_id=callback.from_user.id,
                         title=skill_name)

        builder = InlineKeyboardBuilder()

        builder.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_pagination"))

        await callback.message.answer(text="Вы успешно добавили навык в свою коллекцию",
                                      reply_markup=builder.as_markup())

@router.callback_query(F.data=="back_to_pagination")
async def back_to_pagination(callback: types.CallbackQuery):
    async for session in get_db():
        try:
            await callback.message.delete()
        except:
            pass

        items = await get_skill_pagination(session=session, page=1, user_id=callback.from_user.id)
        total_items = await get_total_items(session=session, user_id=callback.from_user.id)
        total_pages = max(1, (total_items + 4) // 5)
        builder = InlineKeyboardBuilder()

        for i in items:
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f"add_skill_{i}"))

        buttons = []
        if total_pages > 1:
            buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"next_2"))

        if buttons:
            builder.row(*buttons)

        builder.row(types.InlineKeyboardButton(
            text="Отмена",
            callback_data="back_to_start"
        ))

        await callback.message.answer(
            f"Выберите навык из выделенных чтобы добавить в список твоих навыков:\n Страница 1/{total_pages}",
            reply_markup=builder.as_markup()
        )
