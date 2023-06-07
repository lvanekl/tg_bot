from db_class import DB
from env import DB_PATH
from testing.test_utils import load_test_data

my_db = DB(DB_PATH)

@load_test_data
def check_today_training(telegram_chat_id: int):
    # Достаем все тренировки (дни недели) для сегондяшнего чата
    # Дальше достаем все отмены тренировок СЕГОДНЯ
    # Дальше все добавления тренировок НА СЕГОДНЯ
    # Дальше все переносы тренировок НА СЕГОДНЯ

    all_trainigs = my_db.get_schedule(telegram_chat_id=telegram_chat_id)
    all_corrections = [dict(zip(my_db.SCHEDULE_CORRECTION_COLUMNS, correction)) for correction in my_db.get_schedule_corrections(telegram_chat_id=telegram_chat_id)]

    print(all_trainigs)
    print(all_corrections)

if __name__ ==  "__main__":
    check_today_training(telegram_chat_id=1111111)