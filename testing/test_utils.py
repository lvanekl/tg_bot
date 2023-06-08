from db.db_class import DB
from env import DB_PATH, DEFAULT_WELCOME_MEME_PATH
from datetime import time as Time, date as Date, timedelta

my_db = DB(DB_PATH)

t_i = 1111111
def_time1 = Time(hour=19, minute=30)
def_time2 = Time(hour=21, minute=30)

today = Date.today()
today_p1 = Date.today() + timedelta(days=1)
today_p2 = Date.today() + timedelta(days=2)
today_m1 = Date.today() - timedelta(days=1)
today_m2 = Date.today() - timedelta(days=2)


def load_test_data(func):
    def wrapper(*args, **kwargs):
        my_db.clear_all_tables()
        my_db.new_chat(telegram_chat_id=t_i)
        my_db.edit_chat_settings(cgat_GPT=0, welcome_meme=DEFAULT_WELCOME_MEME_PATH)

        my_db.add_gym(telegram_chat_id=t_i, name="gym1")
        my_db.add_gym(telegram_chat_id=t_i, name="gym2")

        # достанем айдишники новых залов
        current_gyms = my_db.get_gyms(telegram_chat_id=1111111)
        g1 = current_gyms[0][0]
        g2 = current_gyms[1][0]

        my_db.add_schedule(telegram_chat_id=t_i, weekday=2, sport="s1", gym=g1, time=def_time1)
        my_db.add_schedule(telegram_chat_id=t_i, weekday=6, sport="s2", gym=g1, time=def_time2)
        my_db.add_schedule(telegram_chat_id=t_i, weekday=1, sport="s2", gym=g2, time=def_time2)
        my_db.add_schedule(telegram_chat_id=t_i, weekday=4, sport="s1", gym=g2, time=def_time1)

        my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="move",
                                      old_date=today, old_time=def_time1, old_gym=g1,
                                      new_date=today_p1, new_time=def_time1, new_gym=g2)
        # такого сдвига быть не может - неверный old_time
        # my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="move",
        #                               old_date=today, old_time=def_time2, old_gym=g1,
        #                               new_date=today_p1, new_time=def_time1, new_gym=g2)

        my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="remove",
                                      old_date=today_p2, old_time=def_time2, old_gym=g1)
        my_db.add_schedule_correction(telegram_chat_id=t_i, correction_type="add",
                                      new_date=today_m1, new_time=def_time2, new_gym=g1)
        # meme
        # admin
        # answer_alternative
        result = func(*args, **kwargs)
        # my_db.clear_all_tables()

        return result

    return wrapper
