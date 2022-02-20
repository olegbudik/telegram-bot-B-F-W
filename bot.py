# СОЗДАЕМ БОТ

# Импортируем все необходимые библиотеки
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN


# Создаем необходимые переменные
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
