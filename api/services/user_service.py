"""User Service"""

import logging
from google.appengine.ext import ndb
from api.models.user import User
from api.errors import UserNotFound, UserDuplicated


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
        users = User.query().filter(query_filter).get()
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
