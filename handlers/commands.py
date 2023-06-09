from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_not_admins_commands(bot: Bot, chat_id: int):
    return await bot.set_my_commands(
        commands=[
            BotCommand("/needs", "Чтобы добавить расходы на обьязательные расходы"),
            BotCommand("/wants", "Чтобы добавить расходы на приятные расходы")
        ],
        scope=BotCommandScopeChat(chat_id),
    )

async def set_reg_commands(bot: Bot, chat_id: int):
    return await bot.set_my_commands(
        commands=[
            BotCommand("/start", "Чтобы начать или же перезапустить бот"),
            BotCommand("/info", "Чтобы получить информацию"),
            BotCommand("/reg", "Чтобы зарегистрировать данные"),
        ],
        scope=BotCommandScopeChat(chat_id),
    )