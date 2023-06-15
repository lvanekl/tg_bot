import logging
from aiogram import types

from env import LOG_PATH, BOT_USERNAME

from bot.permissions import has_permission

logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


class GymsLogics:
    gym_commands = ["get_gyms", "add_gym", "remove_gym", "edit_gym"]

    def register_gym_logics_routes(self):
        self.dp.register_message_handler(self.gyms_logics_router,
                                         commands=self.gym_commands)


    async def gyms_logics_router(self, message: types.Message):
        funcs = {"get_gyms": self.get_gyms,  # TODO отформатировать вывод
                 "add_gym": self.add_gym,  # TODO добавить ограничения
                 "remove_gym": self.remove_gym,  # TODO
                 "edit_gym": self.edit_gym}  # TODO

        command = message.get_command(pure=True)
        await funcs[command](message)
        # await self.my_bot.send_poll(chat_id=telegram_chat_id, **poll, is_anonymous=False)
        # await self.my_bot.send_poll(chat_id=telegram_chat_id, **poll, is_anonymous=False)

    async def get_gyms(self, message: types.Message):
        gyms = await self.my_db.get_gyms(telegram_chat_id=message.chat.id)
        await self.my_bot.send_message(chat_id=message.chat.id, text=f'{gyms}')

    async def add_gym(self, message: types.Message):
        pass

    async def remove_gym(self, message: types.Message):
        pass

    async def edit_gym(self, message: types.Message):
        pass
