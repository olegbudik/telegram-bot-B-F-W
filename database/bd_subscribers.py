import sqlite3
from bot import bot
from keyboards.keyboards import *


# Создаем базу данных подписок, новостей и подключаемся к ней
database = sqlite3.connect('newsletter.db')
sql = database.cursor()

# создаем таблицу подписчиков
sql.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, city TEXT)""")
database.commit()
# создаем таблицу базы новостей (ссылки на новости)
sql.execute("""CREATE TABLE IF NOT EXISTS news(news_id TEXT PRIMARY KEY, 
                                                news0 TEXT NOT NULL, news1 TEXT NOT NULL, news2 TEXT NOT NULL)""")
database.commit()
print('База данных запущена')

""" ================================== БАЗА ДАННЫХ НОВОСТЕЙ ============================== """


def id_news():
    """ Получаем список идентификатора новостей """
    sql.execute(f'SELECT news_id FROM news')
    id_from_bd = sql.fetchall()
    id_news = [id_from_bd[i][0] for i in range(len(id_from_bd))]
    return id_news


def add_news(func_news, data):
    # Добавляем или обновляем новости в базу новостей
    news_from_bd = id_news()
    if func_news in news_from_bd:
        sql.execute('UPDATE news SET news0=?, news1=?, news2=? WHERE news_id=?', (data[0], data[1], data[2], func_news))
        database.commit()
        print(f"Запись для {func_news} обновлена")
    elif func_news not in news_from_bd:
        sql.execute(f'INSERT INTO news VALUES (?,?,?,?)', (func_news, data[0], data[1], data[2]))
        database.commit()
        print(f'Запись для {func_news} добавлена')


def old_news(func_news):
    sql.execute(f'SELECT news0,news1, news2 FROM news WHERE news_id=?', (func_news,))
    old_news = sql.fetchall()[0]
    return old_news


""" ======================================= БАЗА ПОДПИСКИ =============================== """

def all_users_subscribers():
    """ Получаем список всех подписчиков"""
    sql.execute('SELECT user_id FROM users')
    all_users = sql.fetchall()
    return all_users


def add_new_user(user_id):
    """Добавляем нового подписчика с выбором новостной подписки"""
    new_user = [user_id, '']
    sql.execute('INSERT INTO users VALUES (?,?)', new_user)
    database.commit()
    return "Вы успешно подписались"


def delete_subscriber(user_id):
    """Удаляем подписчика из базы """
    sql.execute('DELETE FROM users WHERE user_id=?', (user_id,))
    database.commit()
    return 0


def status_check_user(user_id, text_0, text_1):
    """Проверяем имеет ли пользователь подписку"""
    sql.execute("SELECT user_id FROM users")
    users = list(sql.fetchall())
    if (user_id,) in users:
        return bot.send_message(chat_id=user_id, text=f'{text_1}', reply_markup=button_kb_2)
    else:
        return bot.send_message(chat_id=user_id, text=f'{text_0}', reply_markup=button_kb_1)


def add_city_weather(user_id, text):
    """ Добавляем локацию погоды в базу данных"""
    sql.execute('UPDATE users SET city = ? WHERE user_id = ?', (text, user_id))
    database.commit()
    return text.title()

def status_user_weather(user_id):
    """ Получаем статус пользователя для погоды"""
    sql.execute("SELECT user_id FROM users")
    user = list(sql.fetchall())
    if (user_id,) in user:
        sql.execute("SELECT city FROM users WHERE user_id= ?", (user_id,))
        city = sql.fetchone()
        return city[0]
    else:
        return 0


def close():
    """Закрываем соединение с базой данных"""
    database.commit()
    print('База данных закрыта')
