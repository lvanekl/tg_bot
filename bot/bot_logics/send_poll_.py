from aiogram import types

from bot.bot_main_file import my_bot, dp, my_db


async def send_poll(telegram_chat_id: int, poll: dict):
    await my_bot.send_message(chat_id=telegram_chat_id, text='aaaaaaa')
