import env
from aiogram import Bot, types, executor, Dispatcher

bot = Bot(token=env.token)
dp = Dispatcher(bot)

@dp .message_handler(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer("test")

if __name__ == "__main__":
    executor.start_polling(dp)

# start
# help

# при добавлении в чат - функция new_chat

# get_gyms (тут будут айдишники для редактирования)
# add_gym
# remove_gym
# edit_gym

# get_schedule
# add_schedule
# remove_schedule
# edit_schedule

# get_schedule_corrections
# add_schedule_correction
# remove_schedule_correction
# edit_schedule_correction

# remove_training
# move_training
# add_training

# add_admin
# delete_admin

# edit_settings
# chat_GPT
# welcome_meme

# TODO
# meme
# add meme
# remove meme
# remove_all_memes
# random meme

# обернуть тесты в pytest
# добавить для времени шаблон,
# чтобы в бд хранить время тренировки в едином формате



# check_for_updates (бот запускается раз в день, поэтому может пропустить перенесенную тренировку)
# добро пожаловать в балдежный клуб. Первое задание - сделай комплимент незнакомцу

# каждый чат имеет свой набор (расписание, варианты ответов, переносы)
# при переносе тренировки проверять, не переносили ли ее снова обратно
# можно включить и выключить рандомные вырианты выбора
# /load_my_settings