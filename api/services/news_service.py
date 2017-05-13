"""News Service"""

import logging
from google.appengine.ext import ndb
from api.models.news import News
from api.services import user_service as UserService


def create_news(news):
    logging.info('[SERVICE]: Creating a new news')
    try:
        news.put()
    except Exception as e:
        raise e
    return news

def get_news(query_filter=None):
    logging.info('[SERVICE]: Getting news')
    if not query_filter:
        news = News.query()
    else:
        news = News.query().filter(query_filter)
    return news

@ndb.transactional
def add_like(key, user_id):
    news = key.get()
    if user_id not in news.likes:
        news.likes.append(user_id)
        news.put()

def like_news(news_id, auth_user):
    try:
        news_id = int(news_id)
        user = UserService.get_user_by_email(auth_user['email'])
        key = ndb.Key('News', news_id)
        add_like(key, user.id)
        UserService.add_news_like(user.id, news_id)
    except Exception as e:
        return 'OK'
    return 'OK'
