import requests
from bs4 import BeautifulSoup
from aiogram import Dispatcher
from config import OPEN_WEATHER_TOKEN
import datetime
from database.bd_weather import bd_weather


HEADERS = {'Accept': '*/*', 'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101Firefox/94.0'}

""" ============================ BIATHLON ============================================"""


def news_biathlon():
    """ Функция получения новостей биатлона с сайта """
    url_biathlon = 'https://www.biathlon.com.ua/'
    r = requests.get(url_biathlon, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    data_link = soup.find('td', class_='center_side').find_all('div', class_='news-item')
    news_link = []
    for link in data_link[0:3]:
        news_link.append(url_biathlon + (link.find_all('a', class_='link')[1]).get('href'))
    return news_link


""" ============================ FOOTBALL ============================================ """


def news_football():
    """ Функция получения новостей футбола с сайта """
    url_football = 'https://football24.ua/novini_futbolu_tag2/'
    r = requests.get(url_football, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    data_link = soup.find_all('a', class_="news-title")
    news_link = []
    for link in data_link[0:3]:
        news_link.append(link.get('href'))
    return news_link


"""=========================================== ПОГОДА ========================================"""


def weather_city(text):
    """ Функция проверки получения правильности локации для погоды """
    city = text
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}'
                     f'&appid={OPEN_WEATHER_TOKEN}&units=metric')
    data_weather = r.json()
    errs = {"cod": "404", "message": "city not found"}
    if data_weather == errs:
        return data_weather, 0
    else:
        return data_weather, city


def weather(data_weather):
    """ Функция получения погоды для заданной локации """
    city = data_weather['name']
    temp = data_weather['main']['temp']
    pressure = data_weather['main']['pressure']
    humidity = data_weather['main']['humidity']
    description_weather = data_weather['weather'][0]['main']
    today = datetime.datetime.now()
    today_string = today.strftime(" %d-%b-%Y ")

    news = (f'Погода на {today_string} для {city}:\n'
            f'Температура:  {int(temp)} C\n'
            f'Давление:  {pressure} мм рт.ст\n'
            f'Влажность:  {humidity} %\n'
            f'Описание:  {bd_weather[description_weather]}\n'
            f'\tХ О Р О Ш Е Г О   Д Н Я!')
    return news


NewsBiathlon = news_biathlon()
NewsFootball = news_football()


def register_handlers_news_link(dp: Dispatcher):
    dp.register_message_handler(weather_city)
    dp.register_message_handler(weather)
