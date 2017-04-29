"""api VALIDATORS"""

import re
import logging
from functools import wraps

from flask import request, jsonify
from api.config import SETTINGS
from api.routes.api import error


EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')


def validate_user_creation(func):
    """User Creation Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        json_data = request.get_json()
        if 'email' not in json_data:
            return error(status=400, detail='Email is required')
        else:
            if not EMAIL_REGEX.match(json_data.get('email')):
                return error(status=400, detail='Email not valid')
        if 'role' in json_data:
            role = json_data.get('role')
            if role not in ROLES:
                return error(status=400, detail='role not valid')
        return func(*args, **kwargs)
    return wrapper
