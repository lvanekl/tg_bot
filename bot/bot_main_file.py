import asyncio
from aiogram.types import InputFile

from env import telegram_token, DB_PATH, NEW_CHAT_MEME_PATH
from aiogram import Bot, types, executor, Dispatcher

from db.db_class import DB
from bot.messages import *

my_bot = Bot(token=telegram_token)
dp = Dispatcher(my_bot)
my_db = DB(DB_PATH)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    chat_id = message.chat.id

    all_chats = await my_db.get_chats()
    for chat in all_chats:
        if chat['telegram_chat_id'] == chat_id:
            await message.answer("Ваш чат уже был добавлен в базу данных ранее и сейчас все должно работать корректно. \
                                \n\nЕсли чето сломалось напишите плз разработчику /feedback_help \
                                \n\nЕсли вы запутались в работе бота можете попробовать кликнуть /help")
            return

    await my_db.new_chat(telegram_chat_id=chat_id)

    photo = InputFile(NEW_CHAT_MEME_PATH)
    await my_bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('''he-he lessgoooo... Тоесть... всем привет!) Чтобы узнать что я умею кликните /help''')


@dp.message_handler(commands=["help", "conception_explanation", "gyms_help", "schedule_help",
                              "chat_settings_help", "feedback_help", "about", "schedule_note"])
async def help_function(message: types.Message):
    help_messages = {'/help': base_help_message,
                     '/conception_explanation': conception_explanation_message,
                     '/gyms_help': gyms_help_message,
                     '/schedule_help': schedule_help_message,
                     '/chat_settings_help': chat_settings_help_message,
                     '/feedback_help': feedback_help_message,
                     '/about': about_message,
                     "/schedule_note": schedule_note_message}
    command = message.text
    await message.answer(help_messages[command], parse_mode='HTML')


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp)


if __name__ == "__main__":
    run_bot()

# при добавлении в чат - функция new_chat и вывести текущие настройки

# TODO
# meme
# add meme
# remove meme
# remove_all_memes
# random meme

# /disclaimer


# check_for_updates (бот запускается раз в день, поэтому может пропустить перенесенную тренировку)
# добро пожаловать в балдежный клуб. Первое задание - сделай комплимент незнакомцу

# можно включить и выключить рандомные вырианты выбора
# /load_my_settings
