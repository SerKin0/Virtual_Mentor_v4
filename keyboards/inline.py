# Импортируем необходимые для создания inline-клавиатуры элементы из библиотеки aiogram.types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Импортируем функцию sort_keyboard_button из модуля keyboards.reply
from keyboards.reply import sort_keyboard_button
from temp.log import logger


def create_inline_keyboard_index(buttons: list, index: str, add_last=0, row_width=2) -> InlineKeyboardMarkup | None:
    """ Функция создает inline-клавиатуру, с переданными именами кнопок

    Args:
        buttons: Список названий кнопок клавиатуры
        index: Индекс клавиатуры (Строка, которая будет добавляться к индексу кнопки)
        add_last: Количество кнопок, которые будут размещены на разных строчках в конце клавиатуры
        row_width: Количество кнопок на строку

    Returns:
        Возвращает markup клавиатуры
    """
    if add_last > len(buttons):
        logger.warning("В inline клавиатуре количество дополнительных кнопок больше чем имеющиеся ")
        # Если количество дополнительных кнопок больше чем имеющихся, возвращаем None
        return None
    else:
        # Формируем разметку
        markup = [
            *sort_keyboard_button(list(
                map(lambda button: InlineKeyboardButton(text=button, callback_data=f"{index}_{button}"),
                    buttons if add_last == 0 else buttons[:-add_last])
            ), row_width),
            *sort_keyboard_button(list(
                map(
                    lambda button: InlineKeyboardButton(text=button, callback_data=f"{index}_{button}"),
                    [] if add_last == 0 else buttons[-add_last:]
                )
            ), row_width=1)
        ]
        return InlineKeyboardMarkup(inline_keyboard=markup)
