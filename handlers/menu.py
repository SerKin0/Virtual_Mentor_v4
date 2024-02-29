from aiogram import Router, F
from aiogram.types import Message

# from database.methods.db.json_methods import read_json_menu

router = Router()


# # Пример создания меню в reply клавиатуре из файла .json.
# # Сравниваем текст из сообщения или нажатой reply клавиатуры с кнопкой перехода на другое меню из файла .json
# @router.message(F.text == read_json_menu("")[-1])
# async def main_menu(message: Message):
#     # Меняем клавиатуру на другую и выводим имя этой клавиатуры
#     await message.answer("Главное меню",
#                          reply_markup=creat_reply_keyboard(read_json_menu("main_menu"), add_first=1, add_last=1))
