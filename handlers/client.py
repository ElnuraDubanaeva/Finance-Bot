from aiogram import types, Dispatcher
from config import admin
from handlers.commands import set_not_admins_commands, set_reg_commands
from keyboards.client_kb import type_markup

async def start_handler(message: types.Message):
    if message.from_user.id not in admin:
        if message.text == "/start" or str(message.text).startswith("/start"):
            await message.answer(
                f"Здравствуйте {message.from_user.first_name}🤗! Добро пожаловать в наш бот!"
                f"\nЯ бот помошник Finance. Чтобы начать вести счет /reg",
                reply_markup=type_markup
            )
            await set_reg_commands(message.bot, message.from_user.id)


async def info_handler(message: types.Message):
    if message.from_user.id not in admin:
        if message.text == "/info" or str(message.text).startswith("/info"):
            await message.answer(
                f"Здравствуйте {message.from_user.first_name}🤗!"
                f"\nЯ бот помошник Finance. Чтобы начать вести счет /reg"
                f"\nОтправляйте все данные которые запрашивает бот."
                f"\nЕсли возникнут вопросы то напишете на номер +996778116934"
            )
async def invests_handler(message: types.Message):
    if message.text == "/invests":
        pass
        

def register_message_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(info_handler, commands=["info"])