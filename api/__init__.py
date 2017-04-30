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
from api.routes.api.v1 import user_endpoints_v1
# from api.routes.api.v2 import user_endpoints...

logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Flask App
app = Flask(__name__)

# Cors settings
CORS(app)

# Blueprint Flask Routing
app.register_blueprint(user_endpoints_v1, url_prefix='/api/v1/user')
# app.register_blueprint(endpoints_v2, url_prefix='/api/v2')


@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail='Internal Server Error')
