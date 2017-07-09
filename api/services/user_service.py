"""User Service"""

import logging
import datetime
from google.appengine.ext import ndb
from api.models.user import User, Stock
from api.errors import UserNotFound, UserDuplicated, GenericStockError
from api.services import stock_service as StockService


def create_user(user):
    logging.info('[SERVICE]: Creating a new user')
    current_user = User.query().filter(User.email == user.email).get()
    if current_user:
        raise UserDuplicated(message='User with email '+ user.email+ ' already exists')
    try:
        user.put()
    except Exception as e:
        raise e
    return user

def get_users(query_filter=None):
    logging.info('[SERVICE]: Getting users')
    if not query_filter:
        users = User.query()
    else:
        users = User.query().filter(query_filter)
    return users

def get_user(user_id):
    logging.info('[SERVICE]: Getting user '+ user_id)
    user = User.get_by_id(int(user_id), use_cache=False, use_memcache=False)
    if not user:
        raise UserNotFound(message='User '+ user_id +' does not exist')
    return user

def get_user_by_email(user_email):
    logging.info('[SERVICE]: Getting user by email '+ user_email)
    user = User.query().filter(User.email == user_email).get()
    if not user:
        raise UserNotFound(message='User '+ user_email +' does not exist')
    return user

def update_user(user_id, new_user):
    logging.info('[SERVICE]: Updating user '+user_id)
    user = User.get_by_id(int(user_id), use_cache=False, use_memcache=False)
    if not user:
        raise UserNotFound(message='User '+ user_id +' does not exist')
    try:
        user.role = new_user.get('role') or user.role
        user.address = new_user.get('address') or user.address
        user.mobile_number = new_user.get('mobile_number') or user.mobile_number
        user.birthdate = datetime.datetime.strptime(new_user.get('birthdate').split('T')[0], "%Y-%m-%d").date() or user.birthdate
        user.put()
    except Exception as e:
        raise e
    return user

def update_me(auth_user, new_user):
    logging.info('[SERVICE]: Updating me '+ auth_user['email'])
    user = User.query().filter(User.email == auth_user['email']).get()
    if not user:
        raise UserNotFound(message='User '+ auth_user['email'] +' does not exist')
    try:
        user.address = new_user.get('address') or user.address
        user.mobile_number = new_user.get('mobile_number') or user.mobile_number
        user.birthdate = datetime.datetime.strptime(new_user.get('birthdate').split('T')[0], "%Y-%m-%d").date() or user.birthdate
        user.put()
    except Exception as e:
        raise e
    return user

def delete_user(user_id):
    logging.info('[SERVICE]: Deleting user '+user_id)
    user = User.get_by_id(int(user_id), use_cache=False, use_memcache=False)
    if not user:
        raise UserNotFound(message='User '+ user_id +' does not exist')
    try:
        user.key.delete()
    except Exception as e:
        raise e
    return user

def add_stocks_to_user(user_id, n_stocks):
    logging.info('[SERVICE]: Adding stocks to a user')
    user = User.get_by_id(int(user_id), use_cache=False, use_memcache=False)
    if not user:
        raise UserNotFound(message='User '+ user_id +' does not exist')
    if n_stocks <= 0 or n_stocks > 4:
        raise GenericStockError(message='Invalid Stock number')
    if len(user.stocks) + n_stocks > 4:
        raise GenericStockError(message='Max number of stocks reached')
    try:
        stocks_ids = StockService.get_stock_ids(n_stocks)
    except Exception as e:
        raise GenericStockError(message='Error in StockInfo')
    try:
        for stockid in stocks_ids:
            stock = Stock(
                stockid=stockid
            )
            stock.put()
            user.stocks.append(stock)
        user.put()
    except Exception as e:
        raise e
    return user

def add_news_like(user_id, news_id):
    logging.info('[SERVICE]: Adding news like')
    user = User.get_by_id(int(user_id), use_cache=False, use_memcache=False)
    try:
        if news_id not in user.news_likes:
            user.news_likes.append(news_id)
            user.put()
    except Exception as e:
        raise e

def add_event_going(user_id, event_id):
    logging.info('[SERVICE]: Adding going to event')
    user = User.get_by_id(int(user_id), use_cache=False, use_memcache=False)
    try:
        if event_id not in user.events_going:
            user.events_going.append(event_id)
            user.put()
    except Exception as e:
        raise e
