from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

type_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=3
).add(
    KeyboardButton("/invests"),
    KeyboardButton("/needs"),
    KeyboardButton("/wants"),
)
not_user_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=2
).add(
    KeyboardButton("/reg"),
    KeyboardButton("/info")
)
submit_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("ДА"), KeyboardButton("НЕТ")
)
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("Отмена"),
)
share_number = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("Share number", request_contact=True)
)
precent = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4).add(
    KeyboardButton(10),
    KeyboardButton(20),
    KeyboardButton(30),
    KeyboardButton(40),
    KeyboardButton(50),
) 