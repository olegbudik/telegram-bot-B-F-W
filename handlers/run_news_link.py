import time
# import asyncio
# from aiogram import Dispatcher


from handlers.news_link import NewsBiathlon, NewsFootball
from database import bd_subscribers as bd
from handlers.newsletter import newsletter_biathlon, newsletter_football


def run_add_news():
    """ Функция первоначального добавления новостей в базу при запуске бота """
    bd.add_news('biathlon', NewsBiathlon)
    bd.add_news('football', NewsFootball)


# Обращения к функции получения новостей с сайтов
async def run_new_news():
    await newsletter_biathlon()
    await newsletter_football()


# Функция запуска таймера новостей
async def time_news():
    count = 0
    run_add_news()
    while True:
        await run_new_news()
        print('Таймер запущен', count)
        time.sleep(5)
        count += 1
