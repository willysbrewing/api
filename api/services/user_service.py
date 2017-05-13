"""User Service"""

import logging
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
        logging.info(users)
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
        user.role = new_user.get('role')
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
        stocks = []
        for stockid in stocks_ids:
            stock = Stock(
                stockid=stockid
            )
            stocks.append(stock)
        user.stocks = stocks
        user.put()
    except Exception as e:
        raise e
    return user
