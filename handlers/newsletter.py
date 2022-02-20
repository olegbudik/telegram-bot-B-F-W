from bot import bot


from handlers import news_link
from database import bd_subscribers as bd


def new_news_biathlon():
    """ Функция получения актуальных новостей биатлона (разница новостей с сайта и базы данных)"""
    new_news = news_link.news_biathlon()
    # print('1-b', new_news)
    old_news = bd.old_news('biathlon')
    # print('2-b', old_news)
    news_newsletter_biathlon = [news for news in new_news if news not in old_news]
    if list(news_newsletter_biathlon):
        bd.add_news('biathlon', new_news)
        return news_newsletter_biathlon
    else:
        return 0


def new_news_football():
    """ Функция получения актуальных новостей футбола (разница новостей с сайта и базы данных)"""
    new_news = news_link.news_football()
    old_news = bd.old_news('football')
    news_newsletter_football = [news for news in new_news if news not in old_news]
    if list(news_newsletter_football):
        bd.add_news('football', new_news)
        return news_newsletter_football
    else:
        return 0


async def newsletter_biathlon():
    """ Функция рассылки новостей биатлона """
    news = new_news_biathlon()
    # print('news-b', news)
    all_users = bd.all_users_subscribers()
    # if news != 0:
    #     for user in all_users:
    #         # print(user)
    #         await bot.send_message(chat_id=user[0], text=news[0])
    if news != 0:
        for user in all_users:
            await bot.send_message(chat_id=user[0], text=news)


async def newsletter_football():
    """ Функция рассылки новостей футбола """
    news = new_news_football()
    # print('news-f', news)
    all_users = bd.all_users_subscribers()
    # if news == 0:
    #     for user in all_users:
    #         await bot.send_message(chat_id=user[0], text='Новостей футбола нет')
    if news != 0:
        for user in all_users:
            # print(user)
            await bot.send_message(chat_id=user[0], text=news)
