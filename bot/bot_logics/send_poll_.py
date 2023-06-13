from aiogram import types

class MyBotSendPollClass:
    async def send_poll(self, telegram_chat_id: int, poll: dict):
        # await self.my_bot.send_message(chat_id=telegram_chat_id, text='aaaaaaa')
        await self.my_bot.send_poll(chat_id=telegram_chat_id, **poll, is_anonymous=False)
