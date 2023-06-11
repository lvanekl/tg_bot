from db.db_class import DB
from env import DB_PATH
from testing.test_utils import load_test_data
from datetime import time as Time, date as Date

my_db = DB(DB_PATH)


@load_test_data
def analyze_schedule_today(telegram_chat_id: int):
    # Достаем все тренировки (дни недели) для сегондяшнего чата
    # Дальше достаем все отмены тренировок СЕГОДНЯ
    # Дальше все добавления тренировок НА СЕГОДНЯ
    # Дальше все переносы тренировок НА СЕГОДНЯ

    all_planned_trainigs = my_db.get_schedule(telegram_chat_id=telegram_chat_id)
    # all_corrections = [dict(zip(my_db.SCHEDULE_CORRECTION_COLUMNS, correction)) for correction in
    #                    my_db.get_schedule_corrections(telegram_chat_id=telegram_chat_id)]
    all_corrections = my_db.get_schedule_corrections(telegram_chat_id=telegram_chat_id)
    all_corrections.sort(key=lambda x: x["date_created"])

    today = Date.today()
    current_weekday = today.weekday()

    today_planned_trainings = [tr for tr in all_planned_trainigs if tr['weekday'] == current_weekday]

    for cor in all_corrections:
        if cor['correction_type'] == 'move':
            if cor['old_date'] == today and cor['new_date'] == today:
                for tr in today_planned_trainings:
                    if tr['time'] == cor['old_time'] and tr['place'] == cor['old_place']:
                        tr['time'] = cor['new_time']
                        tr['place'] = cor['new_place']
            elif cor['new_date'] == today:
                for tr in all_planned_trainigs:
                    if tr['time'] == cor['old_time'] \
                            and tr['place'] == cor['old_place'] \
                            and tr['weekday'] == cor['old_date'].weekday():
                        # если тренировка которую переносят вообще была
                        # (дата [день недели], место, время указаны правильно)
                        today_planned_trainings.append({'id': None, 'chat': telegram_chat_id,
                                                        'sport': tr['sport'],
                                                        'gym': cor['new_place'], 'time': cor['new_time']})
            elif cor['old_date'] == today:
                for tr in today_planned_trainings:
                    if tr['time'] == cor['old_time'] and tr['place'] == cor['old_place']:
                        del tr

        elif cor['correction_type'] == 'remove':
            if cor['old_date'] == today:
                for tr in today_planned_trainings:
                    if tr['time'] == cor['old_time'] and tr['place'] == cor['old_place']:
                        del tr
        elif cor['correction_type'] == 'add':
            if cor['new_date'] == today:
                today_planned_trainings.append({'id': None, 'chat': telegram_chat_id,
                                                'sport': 'любой',
                                                'gym': cor['new_place'], 'time': cor['new_time']})

    # print(all_planned_trainigs)
    # print(all_corrections)
    return today_planned_trainings

def clear_schedule_corrections():
    chats = my_db.get_chats()
    today = Date.today()

    counter = 0
    for chat in chats:
        t_i = chat['telegram_chat_id']
        schedule_corrections = my_db.get_schedule_corrections(telegram_chat_id=t_i)
        for sch_c in schedule_corrections:
            if sch_c['old_date'] < today and sch_c['new_date'] < today:
                my_db.remove_schedule_correction(schedule_correction_id=sch_c['id'])
                counter += 1

    return f"Удалено {counter} устаревших поправок в расписание"

if __name__ == "__main__":
    analyze_schedule_today(telegram_chat_id=1111111)
