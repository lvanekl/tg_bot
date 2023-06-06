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

# remove_train
# move_train
# add_train

# current_schedule_corrections
# remove_schedule_correction

# meme
# add meme
# random meme

# edit_welcome_meme
# delete_welcome_meme
# set_default_welcome_meme
# welcome_meme

# add_admin
# delete_admin




# check_for_updates (бот запускается раз в день, поэтому может пропустить перенесенную тренировку)
# добро пожаловать в балдежный клуб. Первое задание - сделай комплимент незнакомцу

# каждый чат имеет свой набор (расписание, варианты ответов, переносы)
# при переносе тренировки проверять, не переносили ли ее снова обратно
# можно включить и выключить рандомные вырианты выбора
# /load_my_settings