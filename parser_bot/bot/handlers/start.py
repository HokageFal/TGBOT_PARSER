from aiogram import types, Router, F
from aiogram.filters.command import Command
from parser_bot.database.core import get_db
from parser_bot.database.crud import get_user
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    async for session in get_db():
        user = await get_user(session,
                              telegram_id=message.from_user.id,
                              username=message.from_user.username)

        # Reply-клавиатура (обычные кнопки)
        kb = [
            [types.KeyboardButton(text="Добавить навыки в ручную")],
            [types.KeyboardButton(text="Мои навыки")],
            [types.KeyboardButton(text="О проекте")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        # Inline-клавиатура (кнопки под сообщением)
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Мои навыки",
                callback_data="my_skills"
            ),
            types.InlineKeyboardButton(
                text="Добавить навыки в ручную",
                callback_data="add_skills_manual"
            ),
            types.InlineKeyboardButton(
                text="О проекте",
                callback_data="about"
            )
        )
        builder.adjust(1)  # По одной кнопке в строке

        await message.answer(
            f"Приветствуем вас в нашем боте, {message.from_user.username}!",
            reply_markup=keyboard
        )

        await message.answer(
            "Скиньте свое резюме с ключевым словом 'Навыки', чтобы добавить навыки",
            reply_markup=builder.as_markup()
        )

@router.callback_query(F.data=="back_to_start")
async def back_start(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Мои навыки",
            callback_data="my_skills"
        ),
        types.InlineKeyboardButton(
            text="Добавить навыки в ручную",
            callback_data="add_skills_manual"
        ),
        types.InlineKeyboardButton(
            text="О проекте",
            callback_data="about"
        )
    )
    builder.adjust(1)

    await callback.message.answer(
        "Скиньте свое резюме с ключевым словом 'Навыки', чтобы добавить навыки",
        reply_markup=builder.as_markup()
    )