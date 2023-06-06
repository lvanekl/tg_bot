import sqlite3 as sq
import logging

from env import DB_LOG_PATH, DEFAULT_WELCOME_MEME_PATH

logging.basicConfig(level=logging.INFO, filename=DB_LOG_PATH, filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


def connect_to_db_decorator(func):
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


class DB:
    def __init__(self, db_filename: str):
        self.db_filename = db_filename

    @connect_to_db_decorator
    def create_default_tables(self):
        pass

    @connect_to_db_decorator
    def clear_all_tables(self):
        self.cur.execute("DELETE FROM chat")
        self.cur.execute("DELETE FROM gym")
        self.cur.execute("DELETE FROM schedule")
        self.cur.execute("DELETE FROM schedule_correction")
        self.cur.execute("DELETE FROM meme")
        self.cur.execute("DELETE FROM answer_alternative")
        self.cur.execute("DELETE FROM admin")
        return "Все таблицы базы данных были очищены"

    @connect_to_db_decorator
    def new_chat(self, telegram_chat_id: int):
        self.cur.execute("INSERT INTO chat (telegram_chat_id, welcome_meme) VALUES (?, ?)",
                         (telegram_chat_id, DEFAULT_WELCOME_MEME_PATH))
        return "В базу данных бота добавлен новый чат (всем приветики в этом чатике)"

    @connect_to_db_decorator
    def get_gyms(self, telegram_chat_id: int):
        self.cur.execute("SELECT * FROM gym WHERE chat == ?", (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db_decorator
    def add_gym(self, telegram_chat_id: int, name: str, address: str = None):
        self.cur.execute("INSERT INTO gym (name, address, chat) VALUES (?, ?, ?)",
                         (name, address, telegram_chat_id))
        return "Добавлен новый зал"

    @connect_to_db_decorator
    def remove_gym(self, gym_id: int):
        self.cur.execute("DELETE FROM gym WHERE id == ?", (gym_id,))
        return "Зал удален"

    @connect_to_db_decorator
    def edit_gym(self, gym_id: int, name: str = "", address: str = ""):
        if name and address:
            self.cur.execute("UPDATE gym SET name = ?, address = ? WHERE id == ?",
                             (name, address, gym_id,))
            return "Изменены имя и адрес зала"
        elif name:
            self.cur.execute("UPDATE gym SET name = ? WHERE id == ?",
                             (name, gym_id,))
            return "Изменено имя зала"
        elif address:
            self.cur.execute("UPDATE gym SET address = ? WHERE id == ?",
                             (address, gym_id,))
            return "Изменен адрес зала"
        else:
            return "Данные о зале не были изменены: либо вы пытаетесь установить пустые значения " \
                   "(тогда просто отправьте пробел), либо я рукожоп"


    @connect_to_db_decorator
    def get_schedule(self, telegram_chat_id: int):
        self.cur.execute("SELECT * FROM schedule WHERE chat == ? ORDER BY weekday", (telegram_chat_id,))
        return self.cur.fetchall()

    @connect_to_db_decorator
    def add_schedule(self, telegram_chat_id: int, weekday: int, sport: str, gym: int, time: str):
        self.cur.execute("INSERT INTO schedule (chat, weekday, sport, gym, time) VALUES (?, ?, ?, ?, ?)",
                         (telegram_chat_id, weekday, sport, gym, time))
        return "Добавлена новая тренировка в расписание"

    @connect_to_db_decorator
    def remove_schedule(self, schedule_id: int):
        self.cur.execute("DELETE FROM schedule WHERE id == ?", (schedule_id,))
        return "Тренировка удалена из расписания"

    @connect_to_db_decorator
    def edit_schedule(self, schedule_id: int, weekday: int = None,
                      sport: str = None, gym: int = None, time: str = None):
        if not (weekday or sport or gym or time):
            return "Расписание не было изменено (параметны не были переданы)"

        edit_columns_list = []
        if weekday:
            edit_columns_list += [f'weekday = {weekday}']
        if sport:
            edit_columns_list += [f'sport = "{sport}"']
        if gym:
            edit_columns_list += [f'gym = {gym}']
        if time:
            edit_columns_list += [f'time = {time}']

        edit_columns_str = ', '.join(edit_columns_list)

        self.cur.execute(f"UPDATE schedule SET {edit_columns_str} WHERE id == ?", (schedule_id,))
        return ("Рапсисание изменено. Отредактированы следующие поля: " + 'день недели, ' * bool(weekday)
                                                                        + 'тип, ' * bool(sport)
                                                                        + 'спортзал, ' * bool(gym)
                                                                        + 'время, ' * bool(time))[:-2]




    @connect_to_db_decorator
    def delete_welcome_meme(self, picture_obj):
        pass
