import sqlite3 as sq
import logging

from datetime import time as Time, date as Date, datetime as Datetime

from env import DB_LOG_PATH, DEFAULT_WELCOME_MEME_PATH, DEFAULT_CHAT_GPT_FLAG

logging.basicConfig(level=logging.DEBUG, filename=DB_LOG_PATH, filemode="a",
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


def form_an_sql_from_kwargs(start_word: str='', **kwargs):
    edit_columns_list = []
    for key, value in kwargs.items():
        if start_word and key.startswith(start_word):
            key = key.replace(start_word, '', 1)
        if value:
            edit_columns_list += [f'{key} = "{value}"']

    edit_columns_str = ', '.join(edit_columns_list)
    logging.debug(edit_columns_str)
    return edit_columns_str


def return_as_dictionary(columns_variable: str):
    def decorator(func):
        def function_wrapper(*args, **kwargs):
            self = args[0]
            column_names = getattr(self, columns_variable)
            result = func(*args, **kwargs)

            d = [dict(zip(column_names, line)) for line in result]
            return d
        return function_wrapper
    return decorator


class DB:
    def __init__(self, db_filename: str):
        self.db_filename = db_filename
        self.create_default_tables()

        self.TABLES = self.get_table_names()

        self.CHAT_COLUMNS = self.get_column_names("chat")
        self.CHAT_SETTINGS_COLUMNS = self.get_column_names("chat_settings")
        self.GYM_COLUMNS = self.get_column_names("gym")
        self.ADMIN_COLUMNS = self.get_column_names("admin")
        self.ANSWER_ALTERNATIVE_COLUMNS = self.get_column_names("answer_alternative")
        self.MEME_COLUMNS = self.get_column_names("meme")
        self.SCHEDULE_COLUMNS = self.get_column_names("schedule")
        self.SCHEDULE_CORRECTION_COLUMNS = self.get_column_names("schedule_correction")

    @connect_to_db
    def create_default_tables(self):
        pass

    @connect_to_db
    def clear_all_tables(self):
        self.cur.execute('''DELETE FROM "chat"''')
        self.cur.execute('''DELETE FROM "chat_settings"''')
        self.cur.execute('''DELETE FROM "gym"''')
        self.cur.execute('''DELETE FROM "schedule"''')
        self.cur.execute('''DELETE FROM "schedule_correction"''')
        self.cur.execute('''DELETE FROM "meme"''')
        self.cur.execute('''DELETE FROM "answer_alternative"''')
        self.cur.execute('''DELETE FROM "admin"''')
        logging.info("БД очищена")
        return "Все таблицы базы данных были очищены"

    @connect_to_db
    def new_chat(self, telegram_chat_id: int):
        self.cur.execute('''INSERT INTO "chat" (telegram_chat_id) VALUES (?)''',
                         (telegram_chat_id,))
        self.cur.execute('''INSERT INTO "chat_settings" (chat, welcome_meme, chat_GPT) VALUES (?, ?, ?)''',
                         (telegram_chat_id, DEFAULT_WELCOME_MEME_PATH, DEFAULT_CHAT_GPT_FLAG))
        return "В базу данных бота добавлен новый чат (всем приветики в этом чатике)"

    @connect_to_db
    @return_as_dictionary(columns_variable="CHAT_COLUMNS")
    def get_chats(self):
        self.cur.execute('''SELECT * FROM "chat"''')
        return self.cur.fetchall()

    @connect_to_db
    @return_as_dictionary(columns_variable="CHAT_SETTINGS_COLUMNS")
    def get_chat_settings(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "chat_settings" WHERE chat == ?''', (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db
    def edit_chat_settings(self, telegram_chat_id: int, **kwargs):
        # на текущем этапе разработки кваргсы это
        # chat_GPT: int (0 bkb 1), welcome_meme: path

        # Добавление welcome_meme происходит путем передачи сюда пути к картинке.
        # Эту логику я вынесу ближе к написанию бота
        # Удаление welcome_meme происходит путем передачи welcome_meme=None

        # нас устроит если у нас впринципе есть ключи и при этом либо хотябы 1 их них передан
        if not (kwargs.keys() and (any([v != None for v in kwargs.values()]))):
            return "Настройки не были изменены (параметны не были переданы)"

        edit_columns_str = form_an_sql_from_kwargs(**kwargs)

        self.cur.execute(f'''UPDATE "chat_settings" SET {edit_columns_str} WHERE chat == ?''', (telegram_chat_id,))
        return ("Настройки были изменены. Отредактированы следующие поля: " + str(list(kwargs.keys())))

    @connect_to_db
    @return_as_dictionary(columns_variable="GYM_COLUMNS")
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
    @return_as_dictionary(columns_variable="SCHEDULE_COLUMNS")
    def get_schedule(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "schedule" WHERE chat == ? ORDER BY weekday''', (telegram_chat_id,))
        schedule = list(map(list, self.cur.fetchall()))

        i = self.SCHEDULE_COLUMNS.index('time')
        for sh in schedule:
            sh[i] = Time.fromisoformat(sh[i])

        return schedule

    @connect_to_db
    def add_schedule(self, telegram_chat_id: int, weekday: int, sport: str, gym: int, time: Time):
        assert 1 <= weekday <= 7
        self.cur.execute('''INSERT INTO "schedule" (chat, weekday, sport, gym, time) VALUES (?, ?, ?, ?, ?)''',
                         (telegram_chat_id, weekday, sport, gym, str(time)))
        return "Добавлена новая тренировка в расписание"

    @connect_to_db
    def remove_schedule(self, schedule_id: int):
        self.cur.execute('''DELETE FROM "schedule" WHERE id == ?''', (schedule_id,))
        return "Тренировка удалена из расписания"

    @connect_to_db
    def edit_schedule(self, schedule_id: int, new_weekday: int = None,
                      new_sport: str = None, new_gym: int = None, new_time: Time = None):
        if not (new_weekday or new_sport or new_gym or new_time):
            return "Расписание не было изменено (параметны не были переданы)"

        edit_columns_str = form_an_sql_from_kwargs(start_word='new_', new_weekday=new_weekday, new_sport=new_sport,
                                                   new_gym=new_gym, new_time=str(new_time))

        self.cur.execute(f'''UPDATE "schedule" SET {edit_columns_str} WHERE id == ?''', (schedule_id,))
        return ("Рапсисание изменено. Отредактированы следующие поля: " + 'день недели, ' * bool(new_weekday)
                + 'тип, ' * bool(new_sport)
                + 'спортзал, ' * bool(new_gym)
                + 'время, ' * bool(new_time))[:-2]

    @connect_to_db
    @return_as_dictionary(columns_variable="SCHEDULE_CORRECTION_COLUMNS")
    def get_schedule_corrections(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "schedule_correction" WHERE chat == ? ORDER BY date_created''',
                         (telegram_chat_id,))

        schedule_corrections = list(map(list, self.cur.fetchall()))

        old_date_i = self.SCHEDULE_CORRECTION_COLUMNS.index('old_date')
        new_date_i = self.SCHEDULE_CORRECTION_COLUMNS.index('new_date')
        old_time_i = self.SCHEDULE_CORRECTION_COLUMNS.index('old_time')
        new_time_i = self.SCHEDULE_CORRECTION_COLUMNS.index('new_time')

        for sh_c in schedule_corrections:
            if sh_c[old_date_i]:
                sh_c[old_date_i] = Date.fromisoformat(sh_c[old_date_i])
            if sh_c[new_date_i]:
                sh_c[new_date_i] = Date.fromisoformat(sh_c[new_date_i])
            if sh_c[old_time_i]:
                sh_c[old_time_i] = Time.fromisoformat(sh_c[old_time_i])
            if sh_c[new_time_i]:
                sh_c[new_time_i] = Time.fromisoformat(sh_c[new_time_i])

        return schedule_corrections

    @connect_to_db
    def add_schedule_correction(self, telegram_chat_id: int, correction_type: str,
                                old_date: Date = None, old_time: Time = None, old_gym: int = None,
                                new_date: Date = None, new_time: Time = None, new_gym: int = None):
        self.cur.execute('''INSERT INTO "schedule_correction" (chat, date_created, correction_type,
                                                               old_date, old_time, old_gym,
                                                               new_date, new_time, new_gym) 
                                                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (telegram_chat_id, int(Datetime.now().timestamp() * 1000), correction_type,
                          str(old_date) if old_date != None else None,
                          str(old_time) if old_time != None else None, old_gym,
                          str(new_date) if new_date != None else None,
                          str(new_time) if new_time != None else None, new_gym))

        return "Добавлена новая поправка в расписание"

    @connect_to_db
    def remove_schedule_correction(self, schedule_correction_id: int):
        self.cur.execute('''DELETE FROM "schedule_correction" WHERE id == ?''', (schedule_correction_id,))
        return "Поправка в расписание удалена из БД"

    @connect_to_db
    def edit_schedule_correction(self, schedule_correction_id: int, new_correction_type: str,
                                 new_old_date: Date, new_old_time: Time, new_old_gym: int,
                                 new_new_date: Date, new_new_time: Time, new_new_gym: int):

        if not (new_correction_type or new_old_date or new_old_time or new_old_gym
                or new_new_date or new_new_time or new_new_gym):
            return "Поправка в расписание не была изменена (параметны не были переданы)"

        edit_columns_str = form_an_sql_from_kwargs(start_word='new_', new_correction_type=new_correction_type,
                                                   new_old_date=str(new_old_date), new_old_time=str(new_old_time),
                                                   new_old_gym=new_old_gym,
                                                   new_new_date=str(new_new_date), new_new_time=str(new_new_time),
                                                   new_new_gym=new_new_gym)

        self.cur.execute(f'''UPDATE "schedule" SET {edit_columns_str} WHERE id == ?''', (schedule_correction_id,))
        return ("Поправка в рапсисание изменена. Отредактированы следующие поля: " +
                'тип поправки, ' * bool(new_correction_type)
                + 'старая дата, ' * bool(new_old_date) + 'новая дата, ' * bool(new_new_date)
                + 'старое время, ' * bool(new_old_time) + 'новое время, ' * bool(new_new_gym)
                + 'старый спортзал, ' * bool(new_old_gym) + 'новая спортзал, ' * bool(new_new_time))[:-2]

    @connect_to_db
    @return_as_dictionary(columns_variable="ADMIN_COLUMNS")
    def get_admins(self, telegram_chat_id: int):
        self.cur.execute('''SELECT * FROM "admin" WHERE chat == ?''', (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db
    def add_admin(self, telegram_chat_id: int, telegram_user_id: int):
        self.cur.execute('''INSERT INTO "admin" (chat, telegram_user_id) VALUES (?, ?)''', telegram_chat_id,
                         telegram_user_id)

    @connect_to_db
    def remove_admin(self, telegram_chat_id: int, telegram_user_id: int):
        self.cur.execute('''DELETE FROM "admin" WHERE "chat" = ? AND "telegram_user_id" = ?''',
                         telegram_chat_id, telegram_user_id)

    @connect_to_db
    def get_column_names(self, table_name: str):
        self.cur.execute(f'PRAGMA table_info("{table_name}")')
        column_names = [i[1] for i in self.cur.fetchall()]
        return column_names

    @connect_to_db
    def get_table_names(self):
        self.cur.execute('''SELECT * FROM "sqlite_master" WHERE type = "table"''')
        tables = self.cur.fetchall()
        return [table[1] for table in tables]
