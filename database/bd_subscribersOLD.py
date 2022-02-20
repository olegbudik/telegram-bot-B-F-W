import sqlite3
from bot import bot
from keyboards.keyboards import *

class BaseData:
    def __init__(self, database):
        """ Создаем базу данных подписок, новостей и подключаемся к ней"""
        self.database = sqlite3.connect('newsletter')
        self.sql = self.database.cursor()
        # создаем таблицу подписчиков
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, city TEXT)""")
        self.database.commit()
        # создаем таблицу базы новостей (ссылки на новости)
        self.sql.execute("""CREATE TABLE IF NOT EXISTS news(news_id TEXT PRIMARY KEY, 
                                                news0 TEXT NOT NULL, news1 TEXT NOT NULL, news2 TEXT NOT NULL)""")
        self.database.commit()
        print('База данных запущена')

    """ ================================== БАЗА ДАННЫХ НОВОСТЕЙ ============================== """


    def id_news(self):
        """ Получаем список идентификатора новостей """
        self.sql.execute(f'SELECT news_id FROM news')
        id_from_bd = self.sql.fetchall()
        id_news = [id_from_bd[i][0] for i in range(len(id_from_bd))]
        return id_news


    def add_news(self, func_news, data):
        # Добавляем или обновляем новости в базу новостей
        news_from_bd = self.id_news()
        if func_news in news_from_bd:
            self.sql.execute('UPDATE news SET news0=?, news1=?, news2=? WHERE news_id=?',
                             (data[0], data[1], data[2], func_news))
            self.database.commit()
            print(f"Запись для {func_news} обновлена")
        if func_news not in news_from_bd:
            self.sql.execute(f'INSERT INTO news VALUES (?,?,?,?)', (func_news, data[0], data[1], data[2]))
            self.database.commit()
            print(f'Запись для {func_news} добавлена')


    def old_news(self, func_news):
        self.sql.execute('SELECT news0, news1, news2 FROM news WHERE news_id=?', (func_news,))
        old_news = self.sql.fetchone()
        return old_news


    """ ======================================= БАЗА ПОДПИСКИ =============================== """

    def add_new_user(self, user_id):
        """Добавляем нового подписчика с выбором новостной подписки"""
        new_user = [user_id, '']
        self.sql.execute('INSERT INTO users VALUES (?,?)', new_user)
        self.database.commit()
        return "Вы успешно подписались"

    def delete_subscriber(self, user_id):
        """Удаляем подписчика из базы """
        self.sql.execute('DELETE FROM users WHERE user_id=?', (user_id,))
        self.database.commit()
        return 0

    def status_check_user(self, user_id, text_0, text_1):
        """Проверяем имеет ли пользователь подписку"""
        self.sql.execute("SELECT user_id FROM users")
        users = list(self.sql.fetchall())
        if (user_id,) in users:
            return bot.send_message(chat_id=user_id, text=f'{text_1}', reply_markup=button_kb_2)
        else:
            return bot.send_message(chat_id=user_id, text=f'{text_0}', reply_markup=button_kb_1)

    def add_city_weather(self, user_id, text):
        """ Добавляем локацию погоды в базу данных"""
        self.sql.execute('UPDATE users SET city = ? WHERE user_id = ?', (text, user_id))
        self.database.commit()
        return text.title()

    def status_user_weather(self, user_id):
        """ Получаем статус пользователя для погоды"""
        self.sql.execute("SELECT user_id FROM users")
        user = list(self.sql.fetchall())
        if (user_id,) in user:
            self.sql.execute("SELECT city FROM users WHERE user_id= ?", (user_id,))
            city = self.sql.fetchone()
            return city[0]
        else:
            return 0


    def close(self):
        """Закрываем соединение с базой данных"""
        self.database.commit()
        print('База данных закрыта')
