import env
from aiogram import Bot, types, executor, Dispatcher
import aiogram
from messages import *

bot = Bot(token=env.telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer('''he-he lessgoooo ''')
    # TODO


@dp.message_handler(commands=["help", "conception_explanation", "gyms_help", "schedule_help",
                              "chat_settings_help", "feedback_help", "about", "schedule_note"])
async def help(message: types.Message):
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


@dp.message_handler(commands=["get_gyms", "add_gym", "remove_gym", "edit_gym"])
async def gym_messages_handler(message: types.Message):
    funcs = {"/get_gyms": ...,
             "/add_gym": ...,
             "/remove_gym": ...,
             "/edit_gym": ...}
    # TODO

@dp.message_handler(commands=["get_schedule", "add_schedule", "remove_schedule",
                              "edit_schedule", "get_schedule_corrections",
                              "add_schedule_correction", "remove_schedule_correction",
                              "edit_schedule_correction", ])
async def schedule_messages_handler(message: types.Message):
    funcs = {"/get_schedule": ...,
             "/add_schedule": ...,
             "/remove_schedule": ...,
             "/edit_schedule": ...,
             "/get_schedule_corrections": ...,
             "/add_schedule_correction": ...,
             "/remove_schedule_correction": ...,
             "/edit_schedule_correction": ...}
    # TODO


@dp.message_handler(commands=["get_settings", "edit_settings", "add_admin", "remove_admin"])
async def settings_messages_handler(message: types.Message):
    funcs = {"/get_settings": ...,
             "/edit_settings": ...,
             "/add_admin": ...,
             "/remove_admin": ...}
    # TODO


@dp.message_handler(commands=["suggest_a_feature", "report_a_bug"])
async def feedback_messages_handler(message: types.Message):
    funcs = {"/suggest_a_feature": ...,
             "/report_a_bug": ...,}
    # TODO


if __name__ == "__main__":
    executor.start_polling(dp)

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
