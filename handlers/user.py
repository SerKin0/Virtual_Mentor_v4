import speech_recognition as sr

from aiogram import Router, F
from aiogram.types import Message, ContentType

router = Router()


@router.message(F.text == "user")
async def hi_user(message: Message):
    await message.answer("Hi, user")
