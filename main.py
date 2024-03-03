import asyncio
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from handlers.menu import main_menu
from temp.log import start_logger

# from database.methods.db.sqlite_methods import Database
from database.methods.json.json_methods import language_message
from handlers import admin, user, menu

load_dotenv(".env")
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await main_menu(message)
    await message.answer(language_message("start_message"))


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(language_message("help_message"))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    # Import Database inside the function
    from database.methods.db.sqlite_methods import Database
    Database().create_database()

    await dp.start_polling(bot)


if __name__ == "__main__":
    start_logger()
    dp.include_routers(admin.router, user.router, menu.router)
    asyncio.run(main())
