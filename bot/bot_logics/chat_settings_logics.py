import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.permissions import has_permission, permission_denied_message

from env import LOG_PATH, BOT_USERNAME

logging.basicConfig(level=logging.INFO, filename=LOG_PATH, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


class ChatSettingsLogics:
    chat_settings_commands = ["get_chat_settings", "edit_chat_settings",
                              "add_bot_admin", "remove_bot_admin",
                              "get_bot_admins"]

    class AddAdminStateGroup(StatesGroup):
        username = State()
    def register_chat_settings_logics_routes(self):
        self.dp.register_message_handler(self.chat_settings_router,
                                         commands=self.chat_settings_commands)

        # self.dp.register_message_handler(self.add_bot_admin_1,
        #                                  state=self.AddAdminStateGroup.username)

    async def chat_settings_router(self, message: types.Message):
        funcs = {"get_chat_settings": self.get_chat_settings,  # TODO отформатировать вывод
                 "edit_chat_settings": ...,  # TODO добавить ограничения
                 "get_bot_admins": self.get_bot_admins,  # TODO отформатировать вывод
                 "add_bot_admin": self.add_bot_admin,  # TODO добавить ограничения
                 "remove_bot_admin": ...}  # TODO добавить ограничения

        command = message.get_command(pure=True)
        await funcs[command](message=message)

    async def get_chat_settings(self, message: types.Message):
        settings = await self.my_db.get_chat_settings(telegram_chat_id=message.chat.id)
        await self.my_bot.send_message(chat_id=message.chat.id, text=f'''{settings}''')

    async def edit_chat_settings(self, message: types.Message):
        pass

    async def get_bot_admins(self, message: types.Message):
        admins = await self.my_db.get_admins(telegram_chat_id=message.chat.id)
        await self.my_bot.send_message(chat_id=message.chat.id, text=f'{admins}')

    async def add_bot_admin(self, message: types.Message):
        if not await has_permission(chat_id=message.chat.id, message=message, my_db=self.my_db, my_bot=self.my_bot):
            await self.my_bot.send_message(chat_id=message.chat.id, text=permission_denied_message)
            return

        await self.AddAdminStateGroup.username.set()
        await self.my_bot.send_message(chat_id=message.chat.id,
                                       text=f'Введите username нового админа (начинается с символа @). Например {BOT_USERNAME}')

    @dp.message_handler(state=AddAdminStateGroup.username)
    async def add_bot_admin_1(self, message: types.Message, state: FSMContext):

        print(1)
        if len(message.entities) != 1 or message.entities[0]["type"] != "mention":
            await self.my_bot.send_message(chat_id=message.chat.id,
                                           text=f'Введите username нового админа (начинается с символа @. Например {BOT_USERNAME})\n'
                                                f'В тексте сообщения должно быть ровно одно упоминание\n'
                                                f'Чтобы отменить команду нажмите /cancel')
            return
        print(2)
        offset = message.entities[0]["offset"]
        length = message.entities[0]["length"]

        print(3)
        username = message.text[offset:offset + length]
        print(4)
        if username[0] != '@':
            await self.my_bot.send_message(chat_id=message.chat.id,
                                           text=f'Введите username нового админа (начинается с символа @. Например {BOT_USERNAME})\n'
                                                f'В тексте сообщения должно быть ровно одно упоминание\n'
                                                f'Чтобы отменить команду нажмите /cancel')
            return
        print(5)
        # async with state.proxy as data:
        #     pass

        print(6)
        user_id = await self.my_bot.resolve_peer(username)
        print(user_id)
        # await self.my_bot.send_message(chat_id=message.chat.id,
        #                                text=f'{username}, {user_id}')

        # all_chat_users = await self.my_bot.get_chat(chat_id=message.chat.id)
        await self.my_bot.send_message(chat_id=message.chat.id,
                                       text=f'{username}')
        # await self.my_bot.send_message(chat_id=message.chat.id,
        #                                text=f'{"a"}')
        # print(message)
        # print()

    async def remove_bot_admin(self, message: types.Message):
        pass

