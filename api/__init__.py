"""API MODULE"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import logging

from flask import Flask, g
from flask_cors import CORS
from api.config import SETTINGS
from api.routes.api import error
from api.routes.api.v1 import user_endpoints_v1, stock_endpoints_v1, \
    news_endpoints_v1, event_endpoints_v1
# from api.routes.api.v2 import user_endpoints...
import firebase_admin
from google.appengine.ext import ndb

# Logging config
logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Flask App
app = Flask(__name__)

# Cors settings
CORS(app)

# DB Cache Settings
context = ndb.get_context()
context.set_cache_policy(lambda key: key.kind() != 'User')
context.set_memcache_policy(lambda key: key.kind() != 'User')
context.set_memcache_timeout_policy(3600)

# JWT using Firebase Auth
default_app = firebase_admin.initialize_app()

# Blueprint Flask Routing
app.register_blueprint(user_endpoints_v1, url_prefix='/v1/user')
app.register_blueprint(stock_endpoints_v1, url_prefix='/v1/stock')
app.register_blueprint(news_endpoints_v1, url_prefix='/v1/news')
app.register_blueprint(event_endpoints_v1, url_prefix='/v1/event')
# app.register_blueprint(endpoints_v2, url_prefix='/v2')


@app.errorhandler(403)
def forbidden(e):
    logging.error('Forbidden')
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    logging.error('Not Found')
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    logging.error('Method Not Allowed')
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    logging.error('Gone')
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    logging.error('Internal Server Error')
    return error(status=500, detail='Internal Server Error')
