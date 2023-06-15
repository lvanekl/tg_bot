import asyncio

from bot.create_bot import dp
import bot.bot_logics
from schedule_worker.schedule_funcs import MyScheduleClass

import logging
from env import LOG_PATH, DB_PATH, LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


# import threading


async def main():
    my_sch = MyScheduleClass(db_path=DB_PATH)
    my_sch.start_scheduling()
    try:
        my_sch.scheduler.start()
        await dp.start_polling()

    except Exception as e:
        raise e


if __name__ == '__main__':
    asyncio.run(main())
