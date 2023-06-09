from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from services.decorators import validate_int
from database.bot_db import DataBase
from keyboards.client_kb import (
    submit_markup,
    cancel_markup,
    share_number,
    precent
)
from services.count import count


class FSMAdminInfo(StatesGroup):
    fullname = State()
    number = State()
    age = State()
    salary = State()
    invests = State()
    needs = State()
    wants = State()
    username = State()
    submit = State()


async def fsm_start(message: types.Message):
    await FSMAdminInfo.fullname.set()
    await message.answer("Фамилия Имя Отчество: ", reply_markup=cancel_markup)


async def load_fullname(message: types.Message, state: FSMContext):
    if (
        str(message.text).replace(" ", "").isalpha()
        and str(message.text).count(" ") == 2
    ):
        async with state.proxy() as data:
            data["fullname"] = message.text.title()
        await FSMAdminInfo.next()
        await message.answer("Укажите свой WhatsApp номер", reply_markup=share_number)
    else:
        await message.answer(
            "Введите ваше Фамилия Имя Отчество", reply_markup=cancel_markup
        )

async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["number"] = message.contact.phone_number
    await FSMAdminInfo.next()
    await message.answer("Ваш возраст")


@validate_int
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = int(message.text)
    await FSMAdminInfo.next()
    await message.answer("Укажите зарплату за месяц")


@validate_int
async def load_salary(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["salary"] = message.text
    await FSMAdminInfo.next()
    await message.answer(
        "Укажите сколько процентов из 100 хотите оставить на накоплений и инвеститций", reply_markup=precent
        )   


@validate_int
async def load_invests(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["invests"] = message.text
    await FSMAdminInfo.next()
    await message.answer(
        f"Укажите процент на обьязательные платежи (комм. услуги, квартплата, продукты) У вас осталось {100 - int(data['invests'])}", reply_markup=precent
        )


@validate_int
async def load_needs(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["needs"] = message.text
        data["wants"] = 100 - int(data["invests"]) - int(data["needs"])
        data["username"] = f"@{message.from_user.username}"
    await message.answer(
        f'\nФИО: {data["fullname"]}'
        f'\nНомер: {data["number"]} '
        f'\nВозраст: {data["age"]}'
        f'\nИнвестиций: {data["invests"]}% {count(total=data["salary"], precent=data["invests"])} som'
        f'\nОбязательные: {data["needs"]}% {count(total=data["salary"], precent=data["needs"])} som'
        f'\nХотелки: {data["wants"]}% {count(total=data["salary"], precent=data["wants"])} som'
        f'\nUsername: {data["username"]}'
    )
    await FSMAdminInfo.next()
    await FSMAdminInfo.next()
    await FSMAdminInfo.next()
    await message.answer("Все данные правильны?", reply_markup=submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await DataBase.insert_info(state)
        await state.finish()
        await message.answer(
            "Регистрация успешно завершена"
            "\n<b> Хорошего дня!</b>🤗 ",
            parse_mode="HTML",
        )
    elif message.text == ["НЕТ", "CANCEL"]:
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


def register_handlers_fsm_users(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=["CANCEL"])
    dp.register_message_handler(
        cancel_reg, Text(equals=["CANCEL", "Отмена"], ignore_case=True), state=["*"]
    )
    dp.register_message_handler(fsm_start, commands=["reg"])
    dp.register_message_handler(load_fullname, state=FSMAdminInfo.fullname)
    dp.register_message_handler(load_number, state=FSMAdminInfo.number, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(load_age, state=FSMAdminInfo.age)
    dp.register_message_handler(load_salary, state=FSMAdminInfo.salary)
    dp.register_message_handler(load_invests, state=FSMAdminInfo.invests)
    dp.register_message_handler(load_needs, state=FSMAdminInfo.needs)
    dp.register_message_handler(submit, state=FSMAdminInfo.submit)