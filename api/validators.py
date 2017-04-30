"""Validators"""

from functools import wraps

from flask import request
from api.schemas import UserSchema
from api.routes.api import error
from api.services import user_service as UserService
from api.errors import UserNotFound
from firebase_admin import auth

def _errors_to_string(errors):
    error = '-'
    for error_key in errors:
        error += error_key + ': ' + errors[error_key][0] + ' -'
    return error


def requires_auth(func):
    """Auth validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify Firebase auth.
        if not request.headers.get('Authorization', None):
            return error(status=401, detail='Unauthorized')
        if len(request.headers.get('Authorization', None).split(' ')) > 2:
            return error(status=401, detail='Unauthorized')
        id_token = request.headers['Authorization'].split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            return error(status=401, detail='Unauthorized')
        if not decoded_token:
            return error(status=401, detail='Unauthorized')
        kwargs['auth_user'] = decoded_token
        return func(*args, **kwargs)
    return wrapper


def requires_admin(func):
    """Admin validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_user = kwargs['auth_user']
        del kwargs['auth_user']
        try:
            user = UserService.get_user_by_email(auth_user.get('email'))
        except UserNotFound:
            return error(status=404, detail='Not Found')
        if user.role != 'ADMIN':
            return error(status=403, detail='Forbidden')
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


def validate_user_update(func):
    """User Update Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        json_data = request.get_json()
        if not json_data:
            return error(status=400, detail='Bad request')
        if not 'role' in json_data:
            return error(status=422, detail='Role missing')
        if json_data.get('role') not in ('USER', 'ADMIN'):
            return error(status=422, detail='Role not valid')
        kwargs['new_user'] = json_data
        return func(*args, **kwargs)
    return wrapper
