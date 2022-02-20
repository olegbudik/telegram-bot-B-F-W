# Импортируем все необходимые библиотеки
import logging
from bot import bot, dp
from aiogram import executor
import asyncio
from config import admin_id
from handlers import news_link, subscribers, run_news_link
# import threading


logging.basicConfig(level=logging.INFO)


subscribers.register_handlers_subscribers(dp)
news_link.register_handlers_news_link(dp)

#  Функция уведомления админа о запуске бота
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


#  Запуск функции старта парсинг новостей
# async def main():
#     task1 = threading.Thread(target=run_news_link.time_news)
#     task1.start()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=send_to_admin)
    # asyncio.run(main())
    asyncio.run(run_news_link.time_news())
