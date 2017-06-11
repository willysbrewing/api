"""News Service"""

import logging
from google.appengine.ext import ndb
from google.appengine.api import memcache
from api.models.news import News
from api.services import user_service as UserService


def create_news(news):
    logging.info('[SERVICE]: Creating a new news')
    try:
        news.put()
        memcache.set(str(news.id), news)
        memcache.delete('news_ids')
    except Exception as e:
        raise e
    return news

def get_news(query_filter=None):
    logging.info('[SERVICE]: Getting news')
    news_ids = memcache.get('news_ids')
    if news_ids is not None:
        news = memcache.get_multi(news_ids)
        if news is not None:
            return news.values()
        else:
            memcache.delete('news_ids')
            return get_news()
    else:
        if not query_filter:
            news = News.query()
        else:
            news = News.query().filter(query_filter)
        news_ids = news.map(lambda news: str(news.id))
        memcache.add('news_ids', news_ids, 3600)
        news_mapping = {}
        for news_el in news:
            news_mapping[str(news_el.id)] = news_el
        memcache.add_multi(news_mapping, 3600)
        return news

@ndb.transactional
def add_like(key, user_id):
    logging.info('[DB]: Transactional')
    news = key.get()
    if user_id not in news.likes:
        news.likes.append(user_id)
        news.put()
        memcache.set(str(news.id), news)

def like_news(news_id, auth_user):
    logging.info('[SERVICE]: Like this news')
    try:
        news_id = int(news_id)
        user = UserService.get_user_by_email(auth_user['email'])
        key = ndb.Key('News', news_id)
        add_like(key, user.id)
        UserService.add_news_like(user.id, news_id)
    except Exception as e:
        return 'OK'
    return 'OK'
