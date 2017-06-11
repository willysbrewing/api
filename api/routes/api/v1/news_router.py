"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import requires_auth, requires_admin, validate_news_creation
from api.services import news_service as NewsService
from api.schemas import NewsSchema
from api.responders import NewsResponder

news_endpoints_v1 = Blueprint('news_endpoints_v1', __name__)

@news_endpoints_v1.route('/', strict_slashes=False, methods=['POST'])
@requires_auth
@requires_admin
@validate_news_creation
def create_news(news):
    """-"""
    logging.info('[ROUTER]: Creating news')
    try:
        # Creating
        news = NewsService.create_news(news)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    news = NewsSchema().dump(news).data
    response = NewsResponder(news).serialize
    return jsonify(data=response), 200

@news_endpoints_v1.route('/', strict_slashes=False, methods=['GET'])
@requires_auth
def get_news(auth_user):
    """-"""
    logging.info('[ROUTER]: Getting news')
    # Getting
    news = NewsService.get_news()
    # Serialize
    news = NewsSchema(many=True).dump(news).data
    response = NewsResponder(news).serialize
    return jsonify(data=response), 200

@news_endpoints_v1.route('/<news_id>/like', strict_slashes=False, methods=['GET'])
@requires_auth
def like_news(news_id, auth_user):
    """-"""
    logging.info('[ROUTER]: Like News')
    # Like new
    NewsService.like_news(news_id, auth_user)
    return jsonify(data='OK'), 200
