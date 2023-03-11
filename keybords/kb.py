from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


button1 = KeyboardButton('/Задачи')

kb_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_button.add(button1)
