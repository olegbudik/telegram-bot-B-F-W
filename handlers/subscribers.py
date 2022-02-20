from bot import bot
from aiogram import types, Dispatcher
from handlers import news_link, run_news_link
from database import bd_subscribers as bd
from keyboards.keyboards import *


# @dp.message_handler(commands='start')
async def send_to_user(message: types.Message):
    text_0 = "Привет!\nМеня зовут BOT_BD! Я могу показать Вам новости биатлона,\nфутбола и " \
             "погоду в указанном городе. Вы также можете\nподписаться на рассылку указанных новостей " \
             "и обновление погоды каждых 6 часов!"
    text_1 = "Вы уже подписаны!"
    await bd.status_check_user(message.from_user.id, text_0, text_1)
    # await run_news_link.time_news()


# @dp.message_handler(commands='Подписаться')
async def subscribe_user(message: types.Message):
    status = bd.add_new_user(message.from_user.id)
    await message.answer(status, reply_markup=button_kb_0)
    await bot.send_message(message.from_user.id, "Введите локацию для прогноза погоды: ", reply_markup=kb_0)


# @dp.message_handler(commands=['Отписаться', 'Отмена'])
async def not_subscribe_user(message: types.Message):
    if bd.delete_subscriber(message.from_user.id) == 0:
        await message.answer("Вы успешно отписались", reply_markup=button_kb_1)


# @dp.message_handler(lambda message: message.text.lower() in ["новости биатлона", "/новости биатлона"])
async def to_news_biathlon(message: types.Message):
    text_0 = text_1 = bd.old_news('biathlon')
    for i in range(2):
        await bd.status_check_user(message.from_user.id, text_0[i], text_1[i])

# @dp.message_handler(lambda message: message.text.lower() in ["новости футбола", "/новости футбола"])
async def to_news_football(message: types.Message):
    text_0 = text_1 = bd.old_news('football')
    for i in range(2):
        await bd.status_check_user(message.from_user.id, text_0[i], text_1[i])


# @dp.message_handler(lambda message: message.text.lower() in ["погода", "/погода"])
async def weather(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вводим локацию: ')
# @dp.message_handler(lambda message: message.text.lower())
async def process_get_weather(message: types.Message):
    data_weather = news_link.weather_city(message.text)
    if data_weather[1] == 0:
        await bot.send_message(message.from_user.id, 'Проверьте локацию: ')
    else:
        weather_city = bd.status_user_weather(message.from_user.id)
        if weather_city == 0:
            text_0 = text_1 = news_link.weather(data_weather[0])
            await bd.status_check_user(message.from_user.id, text_0, text_1)
        else:
            bd.add_city_weather(message.from_user.id, data_weather[1])
            text_0 = text_1 = news_link.weather(data_weather[0])
            await bd.status_check_user(message.from_user.id, text_0, text_1)


def register_handlers_subscribers(dp: Dispatcher):
    dp.register_message_handler(send_to_user, commands=['start'])
    dp.register_message_handler(subscribe_user, commands='Подписаться')
    dp.register_message_handler(not_subscribe_user, commands=['Отписаться', 'Отмена'])
    dp.register_message_handler(to_news_biathlon, lambda message: message.text.lower() in ["новости биатлона",
                                                                                        "/новости биатлона"])
    dp.register_message_handler(to_news_football, lambda message: message.text.lower() in ["новости футбола",
                                                                                        "/новости футбола"])
    dp.register_message_handler(weather, lambda message: message.text.lower() in ["погода", "/погода"])
    dp.register_message_handler(process_get_weather, lambda message: message.text.lower())
