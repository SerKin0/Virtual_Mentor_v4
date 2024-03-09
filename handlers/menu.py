from aiogram import Router, F
from aiogram.types import Message
from database.methods.json.json_methods import language_message

from keyboards import create_reply_keyboard

router = Router()


@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_other_menu", chat)[-1]))
@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_meme_menu", chat)[-1]))
async def main_menu(message: Message):
    # Меняем клавиатуру на другую и выводим имя этой клавиатуры
    await message.answer(language_message("open_start_menu", message),
                         reply_markup=create_reply_keyboard(language_message("buttons_start_menu_private"), add_last=1))


@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_start_menu_private", F)[-1]))
async def other_menu(message: Message):
    # Меняем клавиатуру на другую и выводим имя этой клавиатуры
    await message.answer(language_message("open_other_menu", message),
                         reply_markup=create_reply_keyboard(language_message(
                             "buttons_other_menu", message), add_last=1)
                         )


@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_other_menu", F)[0]))
async def meme_menu(message: Message):
    # Меняем клавиатуру на другую и выводим имя этой клавиатуры
    await message.answer(language_message("open_memes_menu", message),
                         reply_markup=create_reply_keyboard(language_message("buttons_meme_menu"), add_last=1))
