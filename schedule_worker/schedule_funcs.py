import time

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.bot_logics.send_poll_ import send_poll
from db.db_class import DB
from utils.poll_generation import generate_poll
from utils.training_analyzer import analyze_schedule_today, clear_expired_schedule_corrections
from env import DB_PATH, LOG_PATH, SCHEDULE_CHECK_RUN_TIME

from datetime import time as Time, datetime as Datetime

logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
# переменная на случай, если я решу чтото на тестовой бд погонять


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def start_scheduling():
    scheduler.add_job(everyday_schedule_analyzer_testing, trigger='interval', seconds=1)
    scheduler.start()


async def everyday_schedule_analyzer_testing():
    print(1)
    my_db = DB(DB_PATH)
    telegram_chat_id = 409733921

    chat_settings = (await my_db.get_chat_settings(telegram_chat_id=telegram_chat_id))[0]

    await schedule_a_poll_once(telegram_chat_id=telegram_chat_id, chat_settings=chat_settings, training={},
                               send_datetime=Datetime.now())
    print(2)


async def everyday_schedule_analyzer():
    my_db = DB(DB_PATH)
    all_chats = await my_db.get_chats()

    for chat in all_chats:
        chat_settings = (await my_db.get_chat_settings(telegram_chat_id=chat['telegram_chat_id']))[0]
        if chat_settings['auto_poll']:
            await single_chat_analyze_and_send_poll(my_db=my_db, chat=chat, chat_settings=chat_settings,
                                                    send_time=chat_settings['poll_send_time'])

    await clear_expired_schedule_corrections(db_path=DB_PATH)


async def single_chat_analyze_and_send_poll(my_db: DB, chat: dict, chat_settings: dict, send_time: Time):
    all_planned_trainigs = await my_db.get_schedule(telegram_chat_id=chat['telegram_chat_id'])
    all_corrections = await my_db.get_schedule_corrections(telegram_chat_id=chat['telegram_chat_id'])

    today_trainings = await analyze_schedule_today(chat['telegram_chat_id'],
                                                   all_planned_trainigs=all_planned_trainigs,
                                                   all_corrections=all_corrections)

    if today_trainings:
        for tr in today_trainings:
            await schedule_a_poll_once(telegram_chat_id=chat['telegram_chat_id'], chat_settings=chat_settings,
                                       training=tr,
                                       send_datetime=Datetime.combine(Datetime.today(), send_time))


async def schedule_a_poll_once(telegram_chat_id: int, chat_settings: dict, training: dict, send_datetime: Datetime):
    # параметр send_datetime нужен на случай,
    # если отключена автоотправка голосования и люди в чате хотят отправлять ее через /poll

    # poll = await generate_poll(telegram_chat_id, chat_settings=chat_settings, training=training, db_path=DB_PATH)

    # TODO
    scheduler.add_job(send_poll, trigger='date', run_date=send_datetime, kwargs={"telegram_chat_id": telegram_chat_id,
                                                                                 # "poll": poll
                                                                                 "poll": []
                                                                                 })

    # scheduler.add_job(send_poll, trigger='date', run_date=send_datetime, kwargs={"telegram_chat_id": telegram_chat_id,
    #                                                                              "poll": {}})
