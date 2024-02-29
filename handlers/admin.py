from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "admin")
async def hi_admin(message: Message):
    await message.answer("Hi, admin")
