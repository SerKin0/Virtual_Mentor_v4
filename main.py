import asyncio
import logging
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.methods.json.json_methods import language_data_json
from handlers import admin, user, menu

load_dotenv(".env")
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

# Создание логгера
logger = logging.getLogger(__name__)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(language_data_json("start_message"))


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(language_data_json("help_message"))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    from database.methods.db.sqlite_methods import sqliteStart
    sqliteStart()
    logger.info("start message")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    dp.include_routers(admin.router, user.router, menu.router)

    # Установка уровня логирования
    logger.setLevel(logging.INFO)

    # Добавление обработчика для записи логов в файл
    file_handler = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    asyncio.run(main())
