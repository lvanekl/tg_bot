import asyncio

from db.db_class import DB
from env import TEST_DB_PATH, DEFAULT_WELCOME_MEME_PATH
from datetime import time as Time, date as Date, timedelta

t_i = 1111
def_time1 = Time(hour=19, minute=30)
def_time2 = Time(hour=21, minute=30)

today = Date.today()
today_p1 = Date.today() + timedelta(days=1)
today_p2 = Date.today() + timedelta(days=2)
today_m1 = Date.today() - timedelta(days=1)
today_m2 = Date.today() - timedelta(days=2)


def load_test_data(func):
    async def wrapper(*args, **kwargs):
        my_db = DB(TEST_DB_PATH)
        my_db.clear_all_tables()
        # создадим чат и настройки
        await my_db.new_chat(telegram_chat_id=t_i)

        # создадим залы
        g1 = (await my_db.add_gym(telegram_chat_id=t_i, name="gym1"))[0]
        g2 = (await my_db.add_gym(telegram_chat_id=t_i, name="gym2"))[0]

        # создадим расписание
        sch1 = (await my_db.add_schedule(telegram_chat_id=t_i, weekday=2, sport="s1", gym=g1, time=def_time1))[0]
        sch2 = (await my_db.add_schedule(telegram_chat_id=t_i, weekday=7, sport="s2", gym=g1, time=def_time2))[0]
        sch3 = (await my_db.add_schedule(telegram_chat_id=t_i, weekday=1, sport="s2", gym=g2, time=def_time2))[0]
        sch4 = (await my_db.add_schedule(telegram_chat_id=t_i, weekday=4, sport="s1", gym=g2, time=def_time1))[0]

        # создадим несколько поправок в расписание
        sch_c1 = (await my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="move",
                                                      old_date=today, old_time=def_time1, old_gym=g1,
                                                      new_date=today_p1, new_time=def_time1, new_gym=g2))[0]
        sch_c2 = (await my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="remove",
                                                      old_date=today_p2, old_time=def_time2, old_gym=g1))[0]
        sch_c3 = (await my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="add",
                                                      new_date=today_m1, new_time=def_time2, new_gym=g1))[0]
        # answer_alternative
        # meme
        # admin
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)

        my_db.clear_all_tables()

        return result

    return wrapper
