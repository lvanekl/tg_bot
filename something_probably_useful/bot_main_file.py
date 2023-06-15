# import asyncio
# from aiogram.dispatcher import FSMContext
# from aiogram.types import InputFile
#
# # from bot.bot_logics.chat_settings_logics import ChatSettingsLogics
# # from bot.bot_logics.gyms_logics import GymsLogics
# # from bot.bot_logics.polls_logic import PollLogics
# from bot.bot_logics import *
# from env import telegram_token, NEW_CHAT_MEME_PATH, LOG_PATH
# from aiogram import Bot, types, Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
# from db.db_class import DB
# from bot.messages import *
#
# import logging
# logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode="w",
#                     format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
#
#
# def run_bot(db_path: str):
#     global my_db
#     my_db = DB(db_path)
#
#     dp.register_message_handler(start, )
#     dp.register_message_handler(help_function,
#                                 )
#
#     dp.register_message_handler(cancel,)
#
#     # register_chat_settings_logics_routes()
#     # register_gym_logics_routes()
#
# # при добавлении в чат - функция new_chat и вывести текущие настройки
#
# # TODO
# # meme
# # add meme
# # remove meme
# # remove_all_memes
# # random meme
#
# # /disclaimer
#
#
# # check_for_updates (бот запускается раз в день, поэтому может пропустить перенесенную тренировку)
# # добро пожаловать в балдежный клуб. Первое задание - сделай комплимент незнакомцу
#
# # можно включить и выключить рандомные вырианты выбора
# # /load_my_settings
