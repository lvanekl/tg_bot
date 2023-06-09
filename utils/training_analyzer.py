from db.db_class import DB
from datetime import time as Time, date as Date


async def analyze_schedule_today(telegram_chat_id: int, all_planned_trainigs: list, all_corrections: list) -> list:
    all_corrections.sort(key=lambda x: x["date_created"])

    today = Date.today()
    current_weekday = today.weekday()

    today_planned_trainings = [tr for tr in all_planned_trainigs if tr['weekday'] == current_weekday]

    for cor in all_corrections:
        if cor['correction_type'] == 'move':
            if cor['old_date'] == today and cor['new_date'] == today:
                for tr in today_planned_trainings:
                    # если день остается тот же (и это сегодня), то проверяем, что старые время и место те же самые
                    if tr['time'] == cor['old_time'] and tr['gym'] == cor['old_gym']:
                        tr['time'] = cor['new_time']
                        tr['gym'] = cor['new_gym']
            elif cor['new_date'] == today:
                for tr in all_planned_trainigs:
                    if tr['time'] == cor['old_time'] \
                            and tr['gym'] == cor['old_gym'] \
                            and tr['weekday'] == cor['old_date'].weekday():
                        # если тренировка которую переносят на сегодня вообще была
                        # (старые дата [день недели], место, время указаны правильно)
                        today_planned_trainings.append({'id': None, 'chat': telegram_chat_id,
                                                        'sport': tr['sport'],
                                                        'gym': cor['new_gym'], 'time': cor['new_time']})
            elif cor['old_date'] == today:
                for tr in today_planned_trainings:
                    if tr['time'] == cor['old_time'] and tr['gym'] == cor['old_gym']:
                        del tr

        elif cor['correction_type'] == 'remove':
            if cor['old_date'] == today:
                for tr in today_planned_trainings:
                    if tr['time'] == cor['old_time'] and tr['gym'] == cor['old_gym']:
                        del tr
        elif cor['correction_type'] == 'add':
            if cor['new_date'] == today:
                today_planned_trainings.append({'id': None, 'chat': telegram_chat_id,
                                                'sport': 'любой',
                                                'gym': cor['new_gym'], 'time': cor['new_time']})

    today_planned_trainings = [{**dict(s), 'date': today} for s in
                               set(frozenset(d.items()) for d in today_planned_trainings)]

    return today_planned_trainings


async def clear_expired_schedule_corrections(my_db: DB):
    chats = await my_db.get_chats()
    today = Date.today()

    counter = 0
    for chat in chats:
        t_i = chat['telegram_chat_id']
        schedule_corrections = await my_db.get_schedule_corrections(telegram_chat_id=t_i)
        for sch_c in schedule_corrections:
            if sch_c['old_date'] < today and sch_c['new_date'] < today:
                await my_db.remove_schedule_correction(schedule_correction_id=sch_c['id'])
                counter += 1

    return f"Удалено {counter} устаревших поправок в расписание"


# if __name__ == "__main__":
#     analyze_schedule_today(telegram_chat_id=1111111)
