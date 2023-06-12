from env import telegram_token, DB_PATH
from aiogram import Bot, types, executor, Dispatcher

from db.db_class import DB
from messages import *

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)
my_db = DB(DB_PATH)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    print(locals())
    await message.answer('''he-he lessgoooo ''')
    # TODO


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


async def run_bot():
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
