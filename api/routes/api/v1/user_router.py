"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import validate_user_creation, requires_auth
from api.errors import UserNotFound
from api.schemas import UserSchema
from api.responders import UserResponder

user_endpoints_v1 = Blueprint('user_endpoints_v1', __name__)


# USER dump -> serialize / load -> deserialize
@user_endpoints_v1.route('/', strict_slashes=False, methods=['GET'])
@requires_auth
def get_user():
    """-"""
    logging.info('[ROUTER]: Getting user')
    user, error = UserSchema().dump({
        'id': '123',
        'email': 'pepe@pepe.com',
        'first_name': 'Pepe',
        'last_name': 'Perez',
        'gender': 'Male',
        'address': 'Calle de alli'
    })
    response = UserResponder(user).serialize
    return jsonify(data=[response]), 200


@user_endpoints_v1.route('/', strict_slashes=False, methods=['POST'])
@requires_auth
@validate_user_creation
def create_user(user):
    """-"""
    logging.info('[ROUTER]: Creating user')
    response = UserResponder(user).serialize
    return jsonify(data=[response]), 200
