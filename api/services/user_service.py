"""User Service"""

import logging
from google.appengine.ext import ndb
from api.models import User
from api.errors import UserNotFound


def create_user(user):
    logging.info('[SERVICE]: Creating a new user')
    try:
        key = user.put()
    except Exception as e:
        raise e
    user = key.get()
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
    user = User.get_by_id(int(user_id))
    if not user:
        raise UserNotFound(message='User '+ user_id +' does not exist')
    return user

def update_user(user_id, user):
    return {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }

def delete_user(user_id):
    return {
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    }
