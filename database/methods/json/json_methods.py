import json
import logging

language_path = "database/data/json/languages"


def language_data_json(name: str, language="ru") -> list | str:
    """ Читаем json. файлы с названиями кнопок меню и сообщений, возвращаем из них массив

    Args:
        name: Имя меню или сообщения из json файла
        language: Язык сообщения или меню (по умолчанию русский)

    Returns:
        Либо Массив названий кнопок, либо сообщения из файла определенного языка
    """
    with open(f"{language_path}/{language}.json", encoding='utf-8') as f:
        logging.info(name)
        return json.load(f)[name]


def read_json(path: str, data: str):
    """ Возвращает данные из json файлов

    Args:
        path: Путь к json файлу
        data: Данные, которые берем из файла

    Returns:
        Возвращает данные из файла json
    """
    with open(path, encoding='utf-8') as f:
        return json.load(f)[data]


def update_json(path: str, data=None):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
