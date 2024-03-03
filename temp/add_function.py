import difflib


def ifString(string: str, array: list | tuple) -> bool:
    """ Сравнение текста сообщения с вариантами из массива

    Args:
        string: Предложение или слово, которое ищем в массиве вариантов
        array: Массив вариантов

    Returns: Возвращает ответ Да/Нет (True/False)
    """
    string = string.split()  # Разделяем сообщение пользователя на слова через пробел и записываем в массив
    for i in string:  # Перебираем полученный массив
        # Сравниваем слово с вариантами из введённого массива
        if difflib.get_close_matches((str(i)).lower(), array, cutoff=.7):
            return True  # Если в массиве есть хотя бы одно слово из массива возвращаем ИСТИНА
    return False


class Extension:
    def __init__(self):
        pass
