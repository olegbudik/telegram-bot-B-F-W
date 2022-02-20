from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b0 = KeyboardButton('/Отмена')
b1 = KeyboardButton('/Новости биатлона')
b2 = KeyboardButton('/Новости футбола')
b3 = KeyboardButton('/Погода')
b4 = KeyboardButton('/Подписаться')
b5 = KeyboardButton('/Отписаться')

button_kb_0 = ReplyKeyboardRemove()
button_kb_1 = ReplyKeyboardMarkup(resize_keyboard=True)
button_kb_1.add(b1).insert(b2).insert(b3).add(b4)

button_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True)
button_kb_2.add(b3).add(b5)

kb_0 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_0.add(b0)
