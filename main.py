import asyncio

from bot.bot_main_file import MyBot
from schedule_worker.schedule_funcs import MyScheduleClass

import logging
from env import LOG_PATH, DB_PATH

logging.basicConfig(level=logging.DEBUG, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


# import threading


async def main():
    # loop = asyncio.get_event_loop()

    # schedule_thread = threading.Thread(target=asyncio.run, args=(my_sch.start_scheduling(),))
    # schedule_thread.start()
    # schedule_thread.join()
    my_sch = MyScheduleClass(db_path=DB_PATH)
    my_bot = MyBot(db_path=DB_PATH)

    my_sch.start_scheduling()
    try:
        my_sch.scheduler.start()
        # await my_bot.run_bot()
        await my_bot.dp.start_polling()

    except Exception as e:
        raise e


if __name__ == '__main__':
    # try:
    asyncio.run(main())
    # except (KeyboardInterrupt, SystemExit):
    #     logger.error("Bot stopped!")
