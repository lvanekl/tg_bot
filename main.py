import asyncio

from bot.bot_main_file import run_bot
from schedule_worker.schedule_funcs import start_scheduling

import logging
from env import LOG_PATH

logging.basicConfig(level=logging.DEBUG, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')

import threading


def main():
    loop = asyncio.get_event_loop()

    schedule_thread = threading.Thread(target=loop.create_task, args=(start_scheduling(),))
    schedule_thread.start()
    schedule_thread.join()

    # bot_thread = threading.Thread(target=asyncio.run, args=(run_bot(),))
    # bot_thread.start()
    # bot_thread.join()

    loop.run_forever()


if __name__ == "__main__":
    main()
