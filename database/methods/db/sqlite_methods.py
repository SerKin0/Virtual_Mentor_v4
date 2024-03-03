import sqlite3 as sq
from database.methods.json.json_methods import language_message
from keyboards import create_reply_keyboard
from temp.log import logger


async def get_user_data_database(message=None, id_user=None):
    user_info = Database().get_info_user_database(message=message, id_user=id_user)
    # Если данные о пользователе есть, то...
    if user_info:
        # Получаем из .json файла текст сообщения, в которое будет вставляться такие данные как:
        # [0] - Имя, [1] - Фамилия, [3] - Возраст, [5] - Описание пользователя, [6] - Статус/Уровень пользователя,
        # [7] - Язык пользователя
        string = str(language_message("profile_data")) \
            .format(user_info[0], user_info[1], user_info[3], user_info[5],
                    language_message("levels_users")[user_info[6]], user_info[7])

        # Если не был введен ID пользователя, то получаем через message
        id_user = id_user if id_user else message.from_user.id

        # Высылаем сообщение с Данными Пользователя, только в Личные Сообщения
        await message.bot.send_message(id_user, string)
        # Высылаем сообщение с инструкцией для изменения данных пользователей в Личные Сообщения
        await message.bot.send_message(id_user, language_message("edit_profile"))
    # Иначе, возвращаем None
    else:
        return None


class Database:
    def __init__(self):
        self.base = sq.connect('database/data/db/data.db')  # Подключаем файл с базой данных
        self.cur = self.base.cursor()
        self.variants = []
        self.counter = 0

    def create_database(self):
        # Таблица с данными пользователей
        self.base.execute('CREATE TABLE IF NOT EXISTS profile(first_name TEXT, second_name TEXT, username TEXT, '
                          'age INTEGER, id_telegram INTEGER PRIMARY KEY, description TEXT, level INTEGER, '
                          'language TEXT)')
        # Таблица с вопросами пользователей
        self.base.execute('CREATE TABLE IF NOT EXISTS question(id_question INTEGER PRIMARY KEY, id_telegram INTEGER, '
                          'username TEXT, question TEXT)')
        # Таблица с мемами
        self.base.execute('CREATE TABLE IF NOT EXISTS meme(id INTEGER PRIMARY KEY AUTOINCREMENT,img TEXT, text TEXT, '
                          'name TEXT)')

        # Обновление Базы Данных
        self.base.commit()

    # _______________________________________ РАЗДЕЛ ПОЛЬЗОВАТЕЛЬСКИХ ДАННЫХ ___________________________________
    async def add_user_database(self, first_name: str = None, second_name: str = None, username: str = None,
                                age: int = 0, id_telegram: int = None, description: str = None, level: int = None,
                                language: str = None, state=None):
        if state:
            async with state.proxy() as data:
                # Запись в БД с профилями пользователей новый аккаунт
                self.cur.execute('INSERT INTO profile VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
                # Сохранение нового профиля
                self.base.commit()
        else:
            # Запись в БД с профилями пользователей новый аккаунт
            self.cur.execute('INSERT INTO profile VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                             tuple((first_name, second_name, username, age, id_telegram, description, level, language)))
            # Сохранение нового профиля
            self.base.commit()

    # Возвращает массив информации о запрошенном пользователе
    def get_info_user_database(self, message=None, id_user: int = None):
        # Если не был введен ID пользователя, то получаем через message
        id_user = message.from_user.id if not id_user else id_user

        # Получаем данные о пользователе по его id в телеграм и записываем в user_info
        user_info = self.cur.execute(f"SELECT * FROM profile WHERE id_telegram = {id_user}").fetchall()

        # Если есть данные о пользователе, то возвращаем массив, иначе ничего (None)
        return user_info[0] if user_info else None

    async def edit_user_data_database(self, commands: str, edited_information: str, message=None, id_user: int = None):
        # Если не был введен ID пользователя, то получаем через message
        id_user = message.from_user.id if not id_user else id_user

        # Если нет информации о пользователе, то...
        if not self.get_info_user_database(id_user=id_user):
            # Выводим сообщение, что пользователь не зарегистрирован в системе, поэтому не может изменить данные
            await message.answer(language_message("error_edit_data_not_reg", id_user=id_user))

            logger.info(f"Пользователь решил изменить профиля, но он не зарегистрирован")
            return False

        self.cur.execute(f'UPDATE profile SET "{commands}" = "{edited_information}" WHERE id_telegram = {id_user}')
        self.base.commit()
        await message.answer(language_message("edited_data_user", id_user=id_user),
                             reply_markup=create_reply_keyboard(
                                 language_message("buttons_start_menu_private", id_user=id_user))
                             )
        logger.info(f"Пользователь изменил данные профиля: '{commands}' на '{edited_information}'")
        return True

    # ________________________________________________ РАЗДЕЛ МЕМОВ ____________________________________________
    async def get_meme_database(self, message):
        try:
            # Запрашиваем количество мемов в Базе Данных
            count_string = self.cur.execute('SELECT COUNT(id) FROM meme').fetchall()[0][0]
            # Если мы прошлись по всем мемами (либо программа только запустилась), то...
            if self.counter % count_string == 0:
                # Если массив пустой ИЛИ длина нынешнего массива вариантов не равна количеству мемов в БД, то...
                if not self.variants or len(self.variants) != count_string:
                    # Записываем в БД массив с ID мемов
                    self.variants = list(map(lambda x: x[0], self.cur.execute("SELECT id FROM meme").fetchall()))
                # Подключаем функцию для перемешивания случайным образом
                from random import shuffle
                # Перемешиваем массив
                shuffle(self.variants)

            # Выгружаем из БД с мемами строку по ID
            meme = self.cur.execute(
                f'SELECT * FROM meme WHERE id = {self.variants[self.counter % len(self.variants)]}'
            ).fetchall()[0]

            # Переходим на следующий мем
            self.counter += 1

            # Если нет ссылки на изображения, то...
            if not meme[1]:
                # Выводим сообщение только с описанием и ссылкой на автора мема
                await message.answer(f"{meme[1]}\n\n<i>@ {meme[2]}</i>")
            # Иначе...
            else:
                # Записываем описание мема
                description = f"{meme[2]}\n\n" if meme[2] else ""
                # Высылаем фото мема, описание и автора
                await message.bot.send_photo(message.chat.id, meme[1], f"{description}<i>@ {meme[3]}</i>")
        except BaseException:
            # Подключаем функцию для объявления событий
            await message.answer("Прости, мемов пока нет...")
            logger.info("НЕТ МЕМОВ!")

    # Сохраняет вопрос в таблицу
    async def sqlAddQuestion(self, question, message=None, id_question=None, id_telegram=None, username=None):
        if message:
            id_question = message.message_id if not id_question else id_question
            id_telegram = message.from_user.id if not id_telegram else id_telegram
            username = message.from_user.username if not username else username
        array = (id_question, id_telegram, username, question)  # Добавляем во вводимые данные id пользователя и вопрос
        # Записываем в таблицу новый вопрос
        self.cur.execute('INSERT INTO question VALUES (?, ?, ?, ?)', array)
        # Сохраняем изменения
        self.base.commit()

    def all_question_database(self, column="*"):
        return self.cur.execute(f"SELECT {column} FROM question").fetchall()

    def language_user(self, message=None, id_user=None):
        if not (message or id_user):
            # self.self.error("Запросили язык пользователя, но дали пустые message И id_user")
            return "ru"
        id_user = message.from_user.id if not id_user else id_user
        language = self.cur.execute(f"SELECT language FROM profile WHERE id_telegram = {id_user}").fetchall()[0][0]
        if language:
            return language
        else:
            if message:
                return message.from_user.language_code
            else:
                return "ru"

    # Запрашивает данные из любой базы данных
    async def data_from_database(self, name_database, column='*', command=None):
        return self.cur.execute(f'SELECT {column} FROM {name_database} {command}').fetchall()[0]


# async def sqlAddCommand(state):
#     async with state.proxy() as data:
#         print(type(data))
#         cur.execute('INSERT INTO meme VALUES (?, ?, ?, ?)', tuple([None] + list(data.values())))
#         base.commit()
