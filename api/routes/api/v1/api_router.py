"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import validate_user_creation
from api.errors import UserNotFound


endpoints_v1 = Blueprint('endpoints_v1', __name__)


# USER
@endpoints_v1.route('/', strict_slashes=False, methods=['GET'])
def create_user():
    """-"""
    logging.info('[ROUTER]: a')
    return jsonify(data={'a':1}), 200
