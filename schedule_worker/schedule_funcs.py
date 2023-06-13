import time

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.bot_main_file import MyBot
from db.db_class import DB
from utils.poll_generation import generate_poll
from utils.training_analyzer import analyze_schedule_today, clear_expired_schedule_corrections
from env import LOG_PATH, SCHEDULE_CHECK_RUN_TIME, DEFAULT_POLL_SEND_TIME

from datetime import time as Time, datetime as Datetime, timedelta

logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


# переменная на случай, если я решу чтото на тестовой бд погонять


class MyScheduleClass:
    def __init__(self, db_path):
        self.scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
        self.my_db = DB(db_path)
        self.loop = asyncio.get_event_loop()
        self.my_bot = MyBot(db_path=db_path)

    def start_scheduling(self):
        self.scheduler.add_job(self.everyday_schedule_analyzer, trigger='cron',
                               hour=SCHEDULE_CHECK_RUN_TIME.hour,
                               minute=SCHEDULE_CHECK_RUN_TIME.minute,
                               second=SCHEDULE_CHECK_RUN_TIME.second)

    # async def everyday_schedule_analyzer_testing(self):
    #     print(1)
    #     telegram_chat_id = 409733921
    #
    #     chat_settings = (await self.my_db.get_chat_settings(telegram_chat_id=telegram_chat_id))[0]
    #
    #     await self.schedule_a_poll_once(telegram_chat_id=telegram_chat_id, chat_settings=chat_settings, training={},
    #                                     send_datetime=Datetime.now())
    #     print(2)

    async def everyday_schedule_analyzer(self):
        all_chats = await self.my_db.get_chats()

        for chat in all_chats:
            chat_settings = (await self.my_db.get_chat_settings(telegram_chat_id=chat['telegram_chat_id']))[0]
            if chat_settings['auto_poll']:
                await self.single_chat_analyze_and_send_poll(chat=chat, chat_settings=chat_settings,
                                                             # send_time=chat_settings['poll_send_time'],
                                                             send_time=DEFAULT_POLL_SEND_TIME, )
        await clear_expired_schedule_corrections(my_db=self.my_db)

    async def single_chat_analyze_and_send_poll(self, chat: dict, chat_settings: dict, send_time: Time):
        all_planned_trainigs = await self.my_db.get_schedule(telegram_chat_id=chat['telegram_chat_id'])
        all_corrections = await self.my_db.get_schedule_corrections(telegram_chat_id=chat['telegram_chat_id'])

        today_trainings = await analyze_schedule_today(chat['telegram_chat_id'],
                                                       all_planned_trainigs=all_planned_trainigs,
                                                       all_corrections=all_corrections)

        if today_trainings:
            for tr in today_trainings:
                await self.schedule_a_poll_once(telegram_chat_id=chat['telegram_chat_id'], chat_settings=chat_settings,
                                                training=tr,
                                                send_datetime=Datetime.combine(Datetime.today(), send_time))

    async def schedule_a_poll_once(self, telegram_chat_id: int, chat_settings: dict, training: dict,
                                   send_datetime: Datetime):
        # параметр send_datetime нужен на случай,
        # если отключена автоотправка голосования и люди в чате хотят отправлять ее через /poll

        poll = await generate_poll(telegram_chat_id, chat_settings=chat_settings, training=training, my_db=self.my_db)

        # TODO
        self.scheduler.add_job(self.my_bot.send_poll, trigger='date', run_date=send_datetime,
                               kwargs={"telegram_chat_id": telegram_chat_id,
                                       "poll": poll
                                       })
