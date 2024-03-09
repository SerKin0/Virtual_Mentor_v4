import asyncio
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import create_reply_keyboard
from temp.log import start_logger

from database.methods.json.json_methods import language_message
from handlers import admin, user, menu, meme

load_dotenv(".env")
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(language_message("start_message"),
                         reply_markup=create_reply_keyboard(
                             language_message("buttons_start_menu_private", message), add_last=1)
                         )


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(language_message("help_message"))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    from database.methods.db.sqlite_methods import Database
    Database().create_database()

    await dp.start_polling(bot)


if __name__ == "__main__":
    start_logger()
    dp.include_routers(admin.router, user.router, menu.router, meme.router)
    asyncio.run(main())
