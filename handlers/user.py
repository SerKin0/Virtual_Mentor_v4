from aiogram import Router, F
from aiogram.types import Message

from database.methods.json.json_methods import language_message

router = Router()


@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_other_menu", chat)[1]))
async def information_authors(message: Message):
    await message.answer(language_message("information_authors", message).format("https://t.me/BotsSerKin0"))
