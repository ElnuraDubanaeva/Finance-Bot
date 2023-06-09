from aiogram.utils import executor
import logging
from config import dp
from database.bot_db import DataBase
from handlers import fsm_needs, fsm_users, fsm_wants, client


async def on_startup(_):
    DataBase.connect_postgres()

client.register_message_handler_client(dp)
fsm_needs.register_handlers_fsm_needs(dp)
fsm_users.register_handlers_fsm_users(dp)
fsm_wants.register_handlers_fsm_wants(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)