"""api VALIDATORS"""

import logging
from functools import wraps

from flask import request
from api.schemas import UserSchema
from api.routes.api import error


def _errors_to_string(errors):
    error = '-'
    for error_key in errors:
        error += error_key + ': ' + errors[error_key][0] + ' -'
    return error


def requires_auth(func):
    """Auth validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # auth = request.authorization
        auth = True
        if not auth:
            return error(status=401, detail='Unauthorized')
        # kwargs['user'] = User.get(User.email == auth.username) @TODO
        return func(*args, **kwargs)
    return wrapper


def validate_user_creation(func):
    """User Creation Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        json_data = request.get_json()
        if not json_data:
            return error(status=400, detail='Bad request')
        user, errors = UserSchema().load(json_data)
        if errors:
            return error(status=422, detail=_errors_to_string(errors))
        kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper
