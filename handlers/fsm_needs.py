from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.bot_db import DataBase
from keyboards.client_kb import (
    submit_markup,
    not_user_markup,
    cancel_markup
)


class FSMAdminNeeds(StatesGroup):
    info = State()
    username = State()
    amount = State()
    submit = State()
    

async def fsm_start(message: types.Message):
    result = await DataBase.get_user_id(username=f"@{message.from_user.username}")
    if result is None:
        await message.answer("Чтобы вести учет сначало пройдите регистрацию /reg",
                             reply_markup=not_user_markup)
    else:
        await FSMAdminNeeds.info.set()
        available = await DataBase.get_user_needs(f"@{message.from_user.username}")
        if available["available"] <= 0:
            await message.answer("У вас не осталось днег")
        await message.answer(
            f"\nОбщая сумма: {available['total']}"
            f"\nОсталось: {available['available']}"
            f"\nПотратили: {available['wasted']}"
            )
        await message.answer("На что потратили?",
                             reply_markup=cancel_markup)

async def load_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["info"] = message.text
        data["username"] = f"@{message.from_user.username}"
    await FSMAdminNeeds.next()
    await FSMAdminNeeds.next()
    await message.answer("Сколько сомов?", 
                         reply_markup=cancel_markup)
    
async def load_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["amount"] = message.text
    await message.answer(
        f'\nНа что: {data["info"]}'
        f'\nСколько: {data["amount"]} '
    )
    await FSMAdminNeeds.next()
    await message.answer("Все данные правильны?", reply_markup=submit_markup)

async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await DataBase.insert_needs(state)
        await state.finish()
        await message.answer(
            "Регистрация успешно завершена"
            "\n<b> Хорошего дня!</b>🤗 ",
            parse_mode="HTML",
        )
    elif message.text in ["НЕТ", "Отмена"]:
        await message.answer(
            "Отмена! Чтобы заново пройти регистрацию нажмите на команду /reg"
        )
        await state.finish()
    else:
        await message.answer("ДА или НЕТ?!")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer("You CANCELED registration. To start again touch to /reg")
        await state.finish()


def register_handlers_fsm_needs(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=["CANCEL"])
    dp.register_message_handler(
        cancel_reg, Text(equals="Отмена", ignore_case=True), state=["*"]
    )
    dp.register_message_handler(fsm_start, commands=["needs"])
    dp.register_message_handler(load_info, state=FSMAdminNeeds.info)
    dp.register_message_handler(load_amount, state=FSMAdminNeeds.amount)
    dp.register_message_handler(submit, state=FSMAdminNeeds.submit)