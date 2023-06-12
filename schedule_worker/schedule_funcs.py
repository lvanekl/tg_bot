import time

import asyncio
import schedule

from db.db_class import DB
from utils.poll_generation import generate_poll
from utils.training_analyzer import analyze_schedule_today, clear_expired_schedule_corrections
from env import DB_PATH

from datetime import time as Time, datetime

# переменная на случай, если я решу чтото на тестовой бд погонять
db_path = DB_PATH


async def start_scheduling():
    schedule.every().day.at('00:00').do(everyday_schedule_analyzer)
    while True:
        schedule.run_pending()
        time.sleep(1)
        print(datetime.now())


async def everyday_schedule_analyzer():
    my_db = DB(db_path)
    all_chats = await my_db.get_chats()

    for chat in all_chats:
        chat_settings = (await my_db.get_chat_settings(chat=chat['id']))[0]
        if chat_settings['auto_poll']:
            await single_chat_analyze_and_send_poll(my_db=my_db, chat=chat, chat_settings=chat_settings,
                                                    send_time=chat_settings['poll_send_time'])

    await clear_expired_schedule_corrections(db_path=db_path)


async def single_chat_analyze_and_send_poll(my_db: DB, chat: dict, chat_settings: dict, send_time: Time):
    all_planned_trainigs = await my_db.get_schedule(telegram_chat_id=chat['id'])
    all_corrections = await my_db.get_schedule_corrections(telegram_chat_id=chat['id'])

    today_trainings = await analyze_schedule_today(chat['telegram_chat_id'],
                                                   all_planned_trainigs=all_planned_trainigs,
                                                   all_corrections=all_corrections)

    if today_trainings:
        for tr in today_trainings:
            await schedule_a_poll_once(telegram_chat_id=chat['id'], chat_settings=chat_settings, training=tr,
                                       send_time=send_time)


async def schedule_a_poll_once(telegram_chat_id: int, chat_settings: dict, training: dict, send_time: Time):
    # параметр send_time нужен на случай,
    # если отключена автоотправка голосования и люди в чате хотят отправлять ее через /poll

    poll = await generate_poll(telegram_chat_id, chat_settings=chat_settings, training=training, db_path=db_path)
    # schedule.every().day.at(send_time).do(send_poll, telegram_chat_id=telegram_chat_id, poll=poll)
    return schedule.CancelJob
