import asyncio

from bot.bot_main_file import run_bot
from schedule_worker.schedule_funcs import start_scheduling

import logging
from env import LOG_PATH

logging.basicConfig(level=logging.DEBUG, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')

import threading


def main():
    schedule_thread = threading.Thread(target=asyncio.run, args=(start_scheduling(),))
    schedule_thread.start()

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    bot_thread.join()


if __name__ == "__main__":
    main()
