import sqlite3 as sq
import logging

from datetime import time as Time, datetime as Datetime

from env import DB_LOG_PATH, DEFAULT_WELCOME_MEME_PATH

logging.basicConfig(level=logging.INFO, filename=DB_LOG_PATH, filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


def connect_to_db(func):
    def function_wrapper(*args, **kwargs):
        self = args[0]
        function_result = "Функция не начала/не завершила выполнение"
        try:
            with sq.connect(self.db_filename) as db_connection:
                self.cur = db_connection.cursor()
                function_result = func(*args, **kwargs)
                logging.debug(f"Успешно отработала функция {func} c параметрами {args, kwargs}")
        except Exception as ex:
            logging.error(ex, exc_info=True)
            logging.warning(f"Функция {func} не сработала c параметрами {args, kwargs}")

        return function_result

    return function_wrapper


def form_an_sql_from_kwargs(start_word='new_', **kwargs):
    edit_columns_list = []
    for key, value in kwargs:
        if key.startswith(start_word):
            key = key.replace(start_word, '', 1)
        if value:
            edit_columns_list += [f'{key} = {value}']

    edit_columns_str = ', '.join(edit_columns_list)
    return edit_columns_str

class DB:
    def __init__(self, db_filename: str):
        self.db_filename = db_filename

    @connect_to_db
    def create_default_tables(self):
        pass

    @connect_to_db
    def clear_all_tables(self):
        self.cur.execute('''DELETE FROM "chat"''')
        self.cur.execute('''DELETE FROM "gym"''')
        self.cur.execute('''DELETE FROM "schedule"''')
        self.cur.execute('''DELETE FROM "schedule_correction"''')
        self.cur.execute('''DELETE FROM "meme"''')
        self.cur.execute('''DELETE FROM "answer_alternative"''')
        self.cur.execute('''DELETE FROM "admin"''')
        return "Все таблицы базы данных были очищены"

    @connect_to_db
    def new_chat(self, telegram_chat_id: int):
        self.cur.execute('''INSERT INTO "chat" (telegram_chat_id) VALUES (?)''',
                         (telegram_chat_id, ))
        self.cur.execute('''INSERT INTO "chat_settings" (chat, welcome_meme, chat_GPT) VALUES (?, ?, ?)''',
                         (telegram_chat_id, DEFAULT_WELCOME_MEME_PATH, False))
        return "В базу данных бота добавлен новый чат (всем приветики в этом чатике)"

    @connect_to_db
    def get_gyms(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "gym" WHERE chat == ?''', (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db
    def add_gym(self, telegram_chat_id: int, name: str, address: str = None):
        self.cur.execute('''INSERT INTO "gym" (name, address, chat) VALUES (?, ?, ?)''',
                         (name, address, telegram_chat_id))
        return "Добавлен новый зал"

    @connect_to_db
    def remove_gym(self, gym_id: int):
        self.cur.execute('''DELETE FROM "gym" WHERE id == ?''', (gym_id,))
        return "Зал удален"

    @connect_to_db
    def edit_gym(self, gym_id: int, name: str = "", address: str = ""):
        if name and address:
            self.cur.execute('''UPDATE "gym" SET name = ?, address = ? WHERE id == ?''',
                             (name, address, gym_id,))
            return "Изменены имя и адрес зала"
        elif name:
            self.cur.execute('''UPDATE "gym" SET name = ? WHERE id == ?''',
                             (name, gym_id,))
            return "Изменено имя зала"
        elif address:
            self.cur.execute('''UPDATE "gym" SET address = ? WHERE id == ?''',
                             (address, gym_id,))
            return "Изменен адрес зала"
        else:
            return "Данные о зале не были изменены: либо вы пытаетесь установить пустые значения " \
                   "(тогда просто отправьте пробел), либо я рукожоп"

    @connect_to_db
    def get_schedule(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "schedule" WHERE chat == ? ORDER BY weekday''', (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db
    def add_schedule(self, telegram_chat_id: int, weekday: int, sport: str, gym: int, time: Time):
        assert 1 <= weekday <= 7
        self.cur.execute('''INSERT INTO "schedule" (chat, weekday, sport, gym, time) VALUES (?, ?, ?, ?, ?)''',
                         (telegram_chat_id, weekday, sport, gym, time))
        return "Добавлена новая тренировка в расписание"

    @connect_to_db
    def remove_schedule(self, schedule_id: int):
        self.cur.execute('''DELETE FROM "schedule" WHERE id == ?''', (schedule_id,))
        return "Тренировка удалена из расписания"

    @connect_to_db
    def edit_schedule(self, schedule_id: int, new_weekday: int = None,
                      new_sport: str = None, new_gym: int = None, new_time: str = None):
        if not (new_weekday or new_sport or new_gym or new_time):
            return "Расписание не было изменено (параметны не были переданы)"

        edit_columns_str = form_an_sql_from_kwargs(new_weekday=new_weekday, new_sport=new_sport,
                                                   new_gym=new_gym, new_time=new_time)

        self.cur.execute(f'''UPDATE "schedule" SET {edit_columns_str} WHERE id == ?''', (schedule_id,))
        return ("Рапсисание изменено. Отредактированы следующие поля: " + 'день недели, ' * bool(new_weekday)
                                                                        + 'тип, ' * bool(new_sport)
                                                                        + 'спортзал, ' * bool(new_gym)
                                                                        + 'время, ' * bool(new_time))[:-2]

    @connect_to_db
    def get_schedule_corrections(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "schedule_correction" WHERE chat == ? ORDER BY date_created''',
                         (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db
    def add_schedule_correction(self, telegram_chat_id: int, correction_type: str,
                                old_date: Datetime, old_time: str, old_gym: int,
                                new_date: Datetime, new_time: str, new_gym: int):
        self.cur.execute('''INSERT INTO "schedule_correction" (chat, date_created, correction_type,
                                                               old_date, old_time, old_gym,
                                                               new_date, new_time, new_gym) 
                                                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (telegram_chat_id, int(Datetime.now().timestamp()), correction_type,
                          old_date, old_time, old_gym,
                          new_date, new_time, new_gym))
        return "Добавлена новая поправка в расписание"

    @connect_to_db
    def remove_schedule_correction(self, schedule_correction_id: int):
        self.cur.execute('''DELETE FROM "schedule_correction" WHERE id == ?''', (schedule_correction_id,))
        return "Поправка в расписание удалена из БД"

    @connect_to_db
    def edit_schedule_correction(self, schedule_correction_id: int, new_correction_type: str,
                                 new_old_date: Datetime, new_old_time: str, new_old_gym: int,
                                 new_new_date: Datetime, new_new_time: str, new_new_gym: int):

        if not (new_correction_type or new_old_date or new_old_time or new_old_gym
                                    or new_new_date or new_new_time or new_new_gym):
            return "Поправка в расписание не была изменена (параметны не были переданы)"

        edit_columns_str = form_an_sql_from_kwargs(new_correction_type=new_correction_type,
                                 new_old_date=new_old_date, new_old_time=new_old_time, new_old_gym=new_old_gym,
                                 new_new_date=new_new_date, new_new_time=new_new_time, new_new_gym=new_new_gym)

        self.cur.execute(f'''UPDATE "schedule" SET {edit_columns_str} WHERE id == ?''', (schedule_correction_id,))
        return ("Поправка в рапсисание изменена. Отредактированы следующие поля: " +
                'тип поправки, ' * bool(new_correction_type)
                + 'старая дата, ' * bool(new_old_date) + 'новая дата, ' * bool(new_new_date)
                + 'старое время, ' * bool(new_old_time) + 'новое время, ' * bool(new_new_gym)
                + 'старый спортзал, ' * bool(new_old_gym) + 'новая спортзал, ' * bool(new_new_time))[:-2]

    @connect_to_db
    def add_admin(self, telegram_chat_id: int, telegram_user_id: int):
        self.cur.execute('''INSERT INTO "admin" (chat, telegram_user_id) VALUES (?, ?)''', telegram_chat_id, telegram_user_id)

    @connect_to_db
    def remove_admin(self, telegram_chat_id: int, telegram_user_id: int):
        self.cur.execute('''DELETE FROM "admin" WHERE "chat" = ? AND "telegram_user_id" = ?''',
                         telegram_chat_id, telegram_user_id)

    def edit_chat_settings(self, telegram_chat_id: int, **kwargs):
        # на текущем этапе разработки кваргсы это
        # chat_GPT: bool, welcome_meme: path

        # Добавление welcome_meme происходит путем передачи сюда пути к картинке.
        # Эту логику я вынесу ближе к написанию бота
        # Удаление welcome_meme происходит путем передачи welcome_meme=None

        if not (kwargs.keys()):
            return "Настройки не были изменены (параметны не были переданы)"

        edit_columns_str = form_an_sql_from_kwargs(**kwargs)

        self.cur.execute(f'''UPDATE "chat_settings" SET {edit_columns_str} WHERE chat == ?''', (telegram_chat_id,))
        return ("Настройки были изменены. Отредактированы следующие поля: " + str(list(kwargs.keys())))

