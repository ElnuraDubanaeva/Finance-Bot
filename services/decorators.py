from aiogram import types
from aiogram.dispatcher import FSMContext

def validate_int(func):
    async def wrapper(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            return await func(message, state)
        else:
            await message.answer("Введите число")
    return wrapper


def validate_procent(func):
    async def wrapper(message: types.Message, state: FSMContext):
        if message.text.isdigit() and message.text < 100 and message.text != 0:
            return await func(message, state)
        else:
            await message.answer("Введите парвильный процент")
    return wrapper