import asyncio
import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from bot.bot_logics.chat_settings_logics import ChatSettingsLogics
from bot.bot_logics.gyms_logics import GymsLogics
from bot.bot_logics.polls_logic import PollLogics
from env import telegram_token, NEW_CHAT_MEME_PATH, LOG_PATH
from aiogram import Bot, types, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db.db_class import DB
from bot.messages import *

logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


class MyBot(PollLogics, GymsLogics, ChatSettingsLogics):
    storage = MemoryStorage()
    my_bot = Bot(token=telegram_token, parse_mode='HTML')
    dp = Dispatcher(my_bot, storage=storage)

    def __init__(self, db_path: str):

        self.my_db = DB(db_path)
        # self.loop = asyncio.get_event_loop()
        self.dp.register_message_handler(self.start, commands=["start"])
        self.dp.register_message_handler(self.help_function,
                                         commands=["help", "conception_explanation", "gyms_help", "schedule_help",
                                                   "chat_settings_help", "feedback_help", "about", "schedule_note"])

        self.dp.register_message_handler(self.cancel, commands=['cancel'], state="*")

        self.register_chat_settings_logics_routes()
        self.register_gym_logics_routes()


    def run_bot(self):
        executor.start_polling(self.dp)

    async def start(self, message: types.Message):
        chat_id = message.chat.id

        all_chats = await self.my_db.get_chats()
        for chat in all_chats:
            if chat['telegram_chat_id'] == chat_id:
                await message.answer("Ваш чат уже был добавлен в базу данных ранее и сейчас все должно работать корректно. \
                                    \n\nЕсли чето сломалось напишите плз разработчику /feedback_help \
                                    \n\nЕсли вы запутались в работе бота можете попробовать кликнуть /help")
                return

        await self.my_db.new_chat(telegram_chat_id=chat_id)

        photo = InputFile(NEW_CHAT_MEME_PATH)
        await self.my_bot.send_photo(chat_id=message.chat.id, photo=photo)
        await message.answer('''he-he lessgoooo... Тоесть... всем привет!) Чтобы узнать что я умею кликните /help''')

    async def help_function(self, message: types.Message):
        help_messages = {'help': base_help_message,
                         'conception_explanation': conception_explanation_message,
                         'gyms_help': gyms_help_message,
                         'schedule_help': schedule_help_message,
                         'chat_settings_help': chat_settings_help_message,
                         'feedback_help': feedback_help_message,
                         'about': about_message,
                         "schedule_note": schedule_note_message}
        command = message.get_command(pure=True)
        await message.answer(help_messages[command])


    async def cancel(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)
        # Cancel state and inform user about it
        await state.finish()
        # And remove keyboard (just in case)
        await message.reply('Окей, отменяю)', reply_markup=types.ReplyKeyboardRemove())

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
