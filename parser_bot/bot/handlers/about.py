from aiogram import types, Router, F

router = Router()


@router.message(F.text == "О проекте")
async def about_project(message: types.Message):
    try:
        await message.delete()
    except:
        pass

    await message.answer("Информация о проекте...")