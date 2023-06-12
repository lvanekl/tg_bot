import aiosqlite as sq_a
import sqlite3 as sq_s

import logging
from datetime import time as Time, date as Date, datetime as Datetime

from env import DEFAULT_WELCOME_MEME_PATH, DEFAULT_CHAT_FUNNY_QUESTION_FLAG, \
    DEFAULT_CHAT_FUNNY_YES_FLAG, DEFAULT_CHAT_FUNNY_MAYBE_FLAG, DEFAULT_CHAT_FUNNY_NO_FLAG, \
    DEFAULT_AUTO_POLL_FLAG, DEFAULT_POLL_SEND_TIME



def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def check_for_sql_injection(*args, **kwargs):
    # возможно эта функция избыточна. Я прочитал в интернете, что cur.execute("...?...", (arg1, arg2, ...))
    # уже дает проверку на sql инъекции, а у меня почти все написано через него
    # TODO
    pass


def connect_to_db_async(func):
    async def function_wrapper(*args, **kwargs):
        self = args[0]
        function_result = "Функция не начала/не завершила выполнение"

        if check_for_sql_injection(*args, **kwargs):
            logging.warning(f"{func} c параметрами {args, kwargs} - обнаружена sql инъекция")

        try:
            async with sq_a.connect(self.db_filename) as db_connection_a:
                self.con_a = db_connection_a
                self.con_a.row_factory = dict_factory
                async with db_connection_a.cursor() as cur_a:
                    self.cur_a = cur_a
                    function_result = await func(*args, **kwargs)
                    await db_connection_a.commit()
                    logging.debug(f"Успешно отработала функция {func} c параметрами {args, kwargs}")
        except Exception as ex:
            logging.error(ex, exc_info=True)
            logging.warning(f"Функция {func} не сработала c параметрами {args, kwargs}")

        return function_result

    return function_wrapper


def connect_to_db_sync(func):
    def function_wrapper(*args, **kwargs):
        self = args[0]
        function_result = "Функция не начала/не завершила выполнение"

        if check_for_sql_injection(*args, **kwargs):
            logging.warning(f"{func} c параметрами {args, kwargs} - обнаружена sql инъекция")

        try:
            with sq_s.connect(self.db_filename) as db_connection_s:
                self.con_s = db_connection_s
                self.con_s.row_factory = dict_factory
                cur_s = db_connection_s.cursor()
                self.cur_s = cur_s
                function_result = func(*args, **kwargs)
                logging.debug(f"Успешно отработала функция {func} c параметрами {args, kwargs}")
        except Exception as ex:
            logging.error(ex, exc_info=True)
            logging.warning(f"Функция {func} не сработала c параметрами {args, kwargs}")

        return function_result

    return function_wrapper


def form_an_sql_from_kwargs(start_word: str = '', **kwargs):
    edit_columns_list = []
    for key, value in kwargs.items():
        if start_word and key.startswith(start_word):
            key = key.replace(start_word, '', 1)
        if value is not None:
            edit_columns_list += [f'{key} = "{value}"']

    edit_columns_str = ', '.join(edit_columns_list)
    return edit_columns_str


class DbTableManager:
    all_create_statements = {
        "admin": '''CREATE TABLE IF NOT EXISTS "admin" (
    	"id"	INTEGER NOT NULL UNIQUE,
    	"chat"	INTEGER NOT NULL,
    	"telegram_user_id"	INTEGER NOT NULL,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE
    )''',
        "answer_alternative": '''CREATE TABLE IF NOT EXISTS "answer_alternative" (
    	"id"	INTEGER NOT NULL UNIQUE,
    	"chat"	INTEGER NOT NULL,
    	"type"	TEXT NOT NULL,
    	"value"	TEXT NOT NULL,
    	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )''',
        "chat": '''CREATE TABLE IF NOT EXISTS "chat" (
    	"telegram_chat_id"	INTEGER NOT NULL UNIQUE,
    	PRIMARY KEY("telegram_chat_id")
    )''',
        "chat_settings": f'''CREATE TABLE IF NOT EXISTS "chat_settings" (
    	"chat"	INTEGER NOT NULL UNIQUE,
    	"welcome_meme"	TEXT DEFAULT "{DEFAULT_WELCOME_MEME_PATH}",
    	"auto_poll"	INTEGER DEFAULT "{DEFAULT_AUTO_POLL_FLAG}",
    	"funny_question"	INTEGER DEFAULT "{DEFAULT_CHAT_FUNNY_QUESTION_FLAG}",
    	"funny_yes"	INTEGER DEFAULT "{DEFAULT_CHAT_FUNNY_YES_FLAG}",
    	"funny_no"	INTEGER DEFAULT "{DEFAULT_CHAT_FUNNY_NO_FLAG}",
    	"funny_maybe"	INTEGER DEFAULT "{DEFAULT_CHAT_FUNNY_MAYBE_FLAG}",
    	"poll_send_time" TEXT DEFAULT "{DEFAULT_POLL_SEND_TIME}",
    	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE
    )''',
        "gym": '''CREATE TABLE IF NOT EXISTS "gym" (
    	"id"	INTEGER NOT NULL UNIQUE,
    	"chat"	INTEGER NOT NULL,
    	"name"	TEXT NOT NULL,
    	"address"	TEXT,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE
    )''',
        "meme": '''CREATE TABLE IF NOT EXISTS "meme" (
    	"id"	INTEGER NOT NULL UNIQUE,
    	"chat"	INTEGER NOT NULL,
    	"picture_path"	TEXT NOT NULL,
    	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )''',
        "schedule": '''CREATE TABLE IF NOT EXISTS "schedule" (
    	"id"	INTEGER NOT NULL UNIQUE,
    	"chat"	INTEGER NOT NULL,
    	"weekday"	INTEGER NOT NULL CHECK("weekday" >= 0 AND "weekday" <= 6),
    	"sport"	TEXT NOT NULL,
    	"gym"	INTEGER NOT NULL,
    	"time"	TEXT NOT NULL,
    	FOREIGN KEY("gym") REFERENCES "gym"("id") ON DELETE CASCADE,
    	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )''',
        "schedule_correction": '''CREATE TABLE IF NOT EXISTS "schedule_correction" (
    	"id"	INTEGER NOT NULL UNIQUE,
    	"chat"	INTEGER NOT NULL,
    	"date_created"	INTEGER NOT NULL,
    	"correction_type"	TEXT NOT NULL,
    	"old_date"	TEXT,
    	"old_time"	TEXT,
    	"old_gym"	INTEGER,
    	"new_date"	TEXT,
    	"new_time"	TEXT,
    	"new_gym"	INTEGER,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE,
    	FOREIGN KEY("new_gym") REFERENCES "gym"("id") ON DELETE CASCADE,
    	FOREIGN KEY("old_gym") REFERENCES "gym"("id") ON DELETE CASCADE
    )'''

    }

    @connect_to_db_sync
    def create_default_tables(self):
        for table_name, create_statement in self.all_create_statements.items():
            self.cur_s.execute(create_statement)
        return "таблицы успешно созданы"

    @connect_to_db_sync
    def clear_all_tables(self) -> str:
        for table_name in self.TABLES:
            self.cur_s.execute(f'''DELETE FROM "{table_name}"''')
        logging.info("БД очищена")
        return "Все таблицы базы данных были очищены"

    @connect_to_db_sync
    def get_column_names(self, table_name: str) -> list:
        self.cur_s.execute(f'PRAGMA table_info("{table_name}")')
        column_names = [i['name'] for i in self.cur_s.fetchall()]
        return column_names

    @connect_to_db_sync
    def get_table_names(self) -> list:
        self.cur_s.execute('''SELECT * FROM "sqlite_master" WHERE type = "table"''')
        tables = self.cur_s.fetchall()
        return [table['name'] for table in tables]


class DbChatAndSettingsManager:
    @connect_to_db_async
    async def new_chat(self, telegram_chat_id: int) -> tuple:
        await self.cur_a.execute('''INSERT INTO "chat" (telegram_chat_id) VALUES (?)''',
                                 (telegram_chat_id,))
        await self.cur_a.execute('''INSERT INTO "chat_settings" (chat) VALUES (?)''', (telegram_chat_id,))
        return telegram_chat_id, {"status": "success", "detail": "чат добавлен в базу данных"}

    @connect_to_db_async
    async def get_chats(self) -> list:
        await self.cur_a.execute('''SELECT * FROM "chat"''')
        return await self.cur_a.fetchall()

    @connect_to_db_async
    async def get_chat_settings(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "chat_settings" WHERE chat == ?''', (telegram_chat_id,))
        return await self.cur_a.fetchall()

    @connect_to_db_async
    async def edit_chat_settings(self, telegram_chat_id: int, **kwargs) -> tuple:
        # на текущем этапе разработки кваргсы это
        # chat_GPT: int (0 или 1), welcome_meme: path

        # Добавление welcome_meme происходит путем передачи сюда пути к картинке.
        # Эту логику я вынесу ближе к написанию бота
        # Удаление welcome_meme происходит путем передачи welcome_meme=None

        # нас устроит если у нас впринципе есть ключи и при этом либо хотябы 1 их них передан
        if not (kwargs.keys() and (any([v != None for v in kwargs.values()]))):
            return (
                telegram_chat_id, {"status": "error", "detail": "Параметры не были переданы. Настройки не изменены"})

        edit_columns_str = form_an_sql_from_kwargs(**kwargs)
        await self.cur_a.execute(f'''UPDATE "chat_settings" SET {edit_columns_str} WHERE chat == ?''',
                                 (telegram_chat_id,))
        return (telegram_chat_id, {"status": "success",
                                   "detail": "Настройки были изменены. Отредактированы следующие поля: " + str(
                                       list(kwargs.keys()))})


class DbGymManager:

    @connect_to_db_async
    async def get_gyms(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "gym" WHERE chat == ?''', (telegram_chat_id,))
        return await self.cur_a.fetchall()

    @connect_to_db_async
    async def add_gym(self, telegram_chat_id: int, name: str, address: str = None) -> tuple:
        await self.cur_a.execute('''INSERT INTO "gym" (name, address, chat) VALUES (?, ?, ?)''',
                                 (name, address, telegram_chat_id))
        gym_id = self.cur_a.lastrowid
        return gym_id, {"status": "success", "detail": "зал добавлен в базу данных"}

    @connect_to_db_async
    async def remove_gym(self, gym_id: int) -> tuple:
        await self.cur_a.execute('''DELETE FROM "gym" WHERE id == ?''', (gym_id,))
        return None, {"status": "success", "detail": "зал удален из базы данных"}

    @connect_to_db_async
    async def edit_gym(self, gym_id: int, name: str = "", address: str = "") -> tuple:
        if name and address:
            await self.cur_a.execute('''UPDATE "gym" SET name = ?, address = ? WHERE id == ?''',
                                     (name, address, gym_id,))
            return gym_id, {"status": "success", "detail": "Изменены имя и адрес зала"}
        elif name:
            await self.cur_a.execute('''UPDATE "gym" SET name = ? WHERE id == ?''',
                                     (name, gym_id,))
            return gym_id, {"status": "success", "detail": "Изменено имя зала"}
        elif address:
            await self.cur_a.execute('''UPDATE "gym" SET address = ? WHERE id == ?''',
                                     (address, gym_id,))
            return gym_id, {"status": "success", "detail": "Изменен адрес зала"}
        else:
            return (gym_id, {"status": "error",
                             "detail": "Данные о зале не были изменены: либо вы пытаетесь установить "
                                       "пустые значения (тогда просто отправьте пробел), либо я рукожоп"})


class DbScheduleAndScheduleCorrectionsManager:

    @connect_to_db_async
    async def get_schedule(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "schedule" WHERE chat == ? ORDER BY weekday''', (telegram_chat_id,))
        schedule = await self.cur_a.fetchall()

        for sh in schedule:
            sh['time'] = Time.fromisoformat(sh['time'])

        return schedule

    @connect_to_db_async
    async def add_schedule(self, telegram_chat_id: int, weekday: int, sport: str, gym: int, time: Time) -> tuple:
        assert 1 <= weekday <= 7
        await self.cur_a.execute('''INSERT INTO "schedule" (chat, weekday, sport, gym, time) VALUES (?, ?, ?, ?, ?)''',
                                 (telegram_chat_id, weekday, sport, gym, str(time)))
        schedule_id = self.cur_a.lastrowid
        return schedule_id, {"status": "success", "detail": "Добавлена новая тренировка в расписание"}

    @connect_to_db_async
    async def remove_schedule(self, schedule_id: int) -> tuple:
        await self.cur_a.execute('''DELETE FROM "schedule" WHERE id == ?''', (schedule_id,))
        return None, {"status": "success", "detail": "Тренировка удалена из расписания"}

    @connect_to_db_async
    async def edit_schedule(self, schedule_id: int, new_weekday: int = None,
                            new_sport: str = None, new_gym: int = None, new_time: Time = None) -> tuple:
        if not (new_weekday or new_sport or new_gym or new_time):
            return (
                schedule_id, {"status": "error", "detail": "Расписание не было изменено (параметны не были переданы)"})

        edit_columns_str = form_an_sql_from_kwargs(start_word='new_', new_weekday=new_weekday, new_sport=new_sport,
                                                   new_gym=new_gym, new_time=str(new_time))

        await self.cur_a.execute(f'''UPDATE "schedule" SET {edit_columns_str} WHERE id == ?''', (schedule_id,))
        return (schedule_id, {"status": "success",
                              "detail": ("Рапсисание изменено. Отредактированы следующие поля: "
                                         + 'день недели, ' * bool(new_weekday)
                                         + 'тип, ' * bool(new_sport)
                                         + 'спортзал, ' * bool(new_gym)
                                         + 'время, ' * bool(new_time))[:-2]})

    @connect_to_db_async
    async def get_schedule_corrections(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "schedule_correction" WHERE chat == ? ORDER BY date_created''',
                                 (telegram_chat_id,))

        schedule_corrections = await self.cur_a.fetchall()

        for sh_c in schedule_corrections:
            for key in ['old_date', 'new_date']:
                if sh_c[key]:
                    sh_c[key] = Date.fromisoformat(sh_c[key])
            for key in ['old_time', 'new_time']:
                if sh_c[key]:
                    sh_c[key] = Time.fromisoformat(sh_c[key])

        return schedule_corrections

    @connect_to_db_async
    async def add_schedule_correction(self, telegram_chat_id: int, correction_type: str,
                                      old_date: Date = None, old_time: Time = None, old_gym: int = None,
                                      new_date: Date = None, new_time: Time = None, new_gym: int = None) -> tuple:
        await self.cur_a.execute('''INSERT INTO "schedule_correction" (chat, date_created, correction_type,
                                                               old_date, old_time, old_gym,
                                                               new_date, new_time, new_gym) 
                                                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                 (telegram_chat_id, int(Datetime.now().timestamp() * 1000), correction_type,
                                  str(old_date) if old_date is not None else None,
                                  str(old_time) if old_time is not None else None, old_gym,
                                  str(new_date) if new_date is not None else None,
                                  str(new_time) if new_time is not None else None, new_gym))

        schedule_correction_id = self.cur_a.lastrowid
        return schedule_correction_id, {"status": "success", "detail": "Добавлена новая поправка в расписание"}

    @connect_to_db_async
    async def remove_schedule_correction(self, schedule_correction_id: int) -> tuple:
        await self.cur_a.execute('''DELETE FROM "schedule_correction" WHERE id == ?''', (schedule_correction_id,))
        return None, {"status": "success", "detail": "Поправка в расписание удалена из БД"}

    @connect_to_db_async
    async def edit_schedule_correction(self, schedule_correction_id: int, new_correction_type: str,
                                       new_old_date: Date, new_old_time: Time, new_old_gym: int,
                                       new_new_date: Date, new_new_time: Time, new_new_gym: int) -> tuple:

        if not (new_correction_type or new_old_date or new_old_time or new_old_gym
                or new_new_date or new_new_time or new_new_gym):
            return (schedule_correction_id, {"status": "error",
                                             "detail": "Поправка в расписание не была изменена "
                                                       "(параметны не были переданы)"})
        edit_columns_str = form_an_sql_from_kwargs(start_word='new_', new_correction_type=new_correction_type,
                                                   new_old_date=str(new_old_date), new_old_time=str(new_old_time),
                                                   new_old_gym=new_old_gym,
                                                   new_new_date=str(new_new_date), new_new_time=str(new_new_time),
                                                   new_new_gym=new_new_gym)

        await self.cur_a.execute(f'''UPDATE "schedule" SET {edit_columns_str} WHERE id == ?''',
                                 (schedule_correction_id,))
        return (schedule_correction_id, {"status": "success",
                                         "detail": ("Поправка в рапсисание изменена. Отредактированы следующие поля: "
                                                    + 'тип поправки, ' * bool(new_correction_type)
                                                    + 'старая дата, ' * bool(new_old_date)
                                                    + 'новая дата, ' * bool(new_new_date)
                                                    + 'старое время, ' * bool(new_old_time)
                                                    + 'новое время, ' * bool(new_new_gym)
                                                    + 'старый спортзал, ' * bool(new_old_gym)
                                                    + 'новая спортзал, ' * bool(new_new_time))[:-2]})


class DbAnswerAlternativesManager:

    @connect_to_db_async
    async def get_answer_alternatives(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "answer_alternative" WHERE chat == ?''', (telegram_chat_id,))
        return await self.cur_a.fetchall()

    @connect_to_db_async
    async def add_answer_alternative(self, telegram_chat_id: int, answer_type: str, answer_value: str) -> tuple:
        await self.cur_a.execute('''INSERT INTO "answer_alternative" (chat, type, value) VALUES (?, ?, ?)''',
                                 (telegram_chat_id,
                                  answer_type,
                                  answer_value))

        aa_id = self.cur_a.lastrowid
        return aa_id, {"status": "success", "detail": f"Добавлен вариант ответа: {answer_type} -> {answer_value}"}

    @connect_to_db_async
    async def remove_answer_alternative(self, telegram_chat_id: int, answer_alternative_id: int) -> tuple:
        await self.cur_a.execute('''DELETE FROM "answer_alternative" WHERE "id" = ?''', answer_alternative_id)
        return None, {"status": "success", "detail": f"Удален вариант ответа"}

    async def get_answer_alternatives_grouped_by_types(self, telegram_chat_id: int) -> dict:
        answer_alternatives = await self.get_answer_alternatives(telegram_chat_id)
        # [dict(zip(column_names, line)) for line in result]

        answer_alternatives_grouped_by_types = {}

        for aa in answer_alternatives:
            t = aa["type"]
            v = aa["value"]
            if t not in answer_alternatives_grouped_by_types:
                answer_alternatives_grouped_by_types[t] = []
            answer_alternatives_grouped_by_types[t].append(v)

        return answer_alternatives_grouped_by_types

    @connect_to_db_async
    async def get_answer_alternatives(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "answer_alternative" WHERE chat == ?''', (telegram_chat_id,))
        return await self.cur_a.fetchall()

    @connect_to_db_async
    async def add_answer_alternative(self, telegram_chat_id: int, answer_type: str, answer_value: str) -> tuple:
        await self.cur_a.execute('''INSERT INTO "answer_alternative" (chat, type, value) VALUES (?, ?, ?)''',
                                 (telegram_chat_id,
                                  answer_type,
                                  answer_value))

        aa_id = self.cur_a.lastrowid
        return aa_id, {"status": "success", "detail": f"Добавлен вариант ответа: {answer_type} -> {answer_value}"}

    @connect_to_db_async
    async def remove_answer_alternative(self, telegram_chat_id: int, answer_alternative_id: int) -> tuple:
        await self.cur_a.execute('''DELETE FROM "answer_alternative" WHERE "id" = ?''', answer_alternative_id)
        return None, {"status": "success", "detail": f"Удален вариант ответа"}

    async def get_answer_alternatives_grouped_by_types(self, telegram_chat_id: int) -> dict:
        answer_alternatives = await self.get_answer_alternatives(telegram_chat_id)
        # [dict(zip(column_names, line)) for line in result]

        answer_alternatives_grouped_by_types = {}

        for aa in answer_alternatives:
            t = aa["type"]
            v = aa["value"]
            if t not in answer_alternatives_grouped_by_types:
                answer_alternatives_grouped_by_types[t] = []
            answer_alternatives_grouped_by_types[t].append(v)

        return answer_alternatives_grouped_by_types


class DbAdminManager:

    @connect_to_db_async
    async def get_admins(self, telegram_chat_id: int) -> list:
        await self.cur_a.execute('''SELECT * FROM "admin" WHERE chat == ?''', (telegram_chat_id,))
        return await self.cur_a.fetchall()

    @connect_to_db_async
    async def add_admin(self, telegram_chat_id: int, telegram_user_id: int) -> tuple:
        await self.cur_a.execute('''INSERT INTO "admin" (chat, telegram_user_id) VALUES (?, ?)''', (telegram_chat_id,
                                                                                                    telegram_user_id))
        admin_id = self.cur_a.lastrowid
        return admin_id, {"status": "success", "detail": "В чат добавлен новый админ"}

    @connect_to_db_async
    async def remove_admin(self, telegram_chat_id: int, telegram_user_id: int) -> tuple:
        await self.cur_a.execute('''DELETE FROM "admin" WHERE "chat" = ? AND "telegram_user_id" = ?''',
                                 telegram_chat_id, telegram_user_id)
        return None, {"status": "success", "detail": "Админ удален"}


class DbMemeManager:
    pass
    # TODO memes


class DB(DbTableManager, DbChatAndSettingsManager, DbGymManager,
         DbScheduleAndScheduleCorrectionsManager, DbAnswerAlternativesManager,
         DbAdminManager, DbMemeManager):
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
