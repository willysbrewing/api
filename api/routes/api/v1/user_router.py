"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import validate_user_creation, validate_user_update, \
    requires_auth, requires_admin
from api.services import user_service as UserService
from api.errors import UserNotFound, UserDuplicated
from api.schemas import UserSchema
from api.responders import UserResponder

user_endpoints_v1 = Blueprint('user_endpoints_v1', __name__)

# USER dump -> serialize / load -> deserialize
@user_endpoints_v1.route('/', strict_slashes=False, methods=['POST'])
@requires_auth
@requires_admin
@validate_user_creation
def create_user(user):
    """-"""
    logging.info('[ROUTER]: Creating user')
    try:
        # Creating
        user = UserService.create_user(user)
    except UserDuplicated as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    user = UserSchema().dump(user).data
    response = UserResponder(user).serialize
    return jsonify(data=response), 200

@user_endpoints_v1.route('/', strict_slashes=False, methods=['GET'])
@requires_auth
@requires_admin
def get_users():
    """-"""
    logging.info('[ROUTER]: Getting users')
    # Getting
    users = UserService.get_users()
    # Serialize
    users = UserSchema(many=True).dump(users).data
    response = UserResponder(users).serialize
    return jsonify(data=response), 200

@user_endpoints_v1.route('/<user_id>', strict_slashes=False, methods=['GET'])
@requires_auth
@requires_admin
def get_user(user_id):
    """-"""
    logging.info('[ROUTER]: Getting user')
    try:
        # Getting
        user = UserService.get_user(user_id)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    user = UserSchema().dump(user).data
    response = UserResponder(user).serialize
    return jsonify(data=response), 200

@user_endpoints_v1.route('/<user_id>', strict_slashes=False, methods=['PATCH'])
@requires_auth
@requires_admin
@validate_user_update
def update_user(user_id, new_user):
    """-"""
    logging.info('[ROUTER]: Updating user')
    try:
        # Update
        user = UserService.update_user(user_id, new_user)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    user = UserSchema().dump(user).data
    response = UserResponder(user).serialize
    return jsonify(data=response), 200

@user_endpoints_v1.route('/<user_id>', strict_slashes=False, methods=['DELETE'])
@requires_auth
@requires_admin
def delete_user(user_id):
    """-"""
    logging.info('[ROUTER]: Deleting user')
    try:
        # Update
        user = UserService.delete_user(user_id)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    user = UserSchema().dump(user).data
    response = UserResponder(user).serialize
    return jsonify(data=response), 200

@user_endpoints_v1.route('/me', strict_slashes=False, methods=['GET'])
@requires_auth
def get_me(auth_user):
    """-"""
    logging.info('[ROUTER]: Getting me')
    try:
        # Getting
        user = UserService.get_user_by_email(auth_user.get('email'))
    except UserNotFound as e:
        logging.error('[ROUTER]: Creating for the first time')
        user, errors = UserSchema().load(
            {
                'first_name': auth_user.get('name').split(' ')[0],
                'last_name': auth_user.get('name').split(' ')[1],
                'email': auth_user.get('email')
            }
        )
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    user = UserSchema().dump(user).data
    response = UserResponder(user).serialize
    return jsonify(data=response), 200
