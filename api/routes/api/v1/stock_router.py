"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import requires_auth, requires_admin
from api.services import stock_service as StockService
from api.responders import StockInfoResponder

stock_endpoints_v1 = Blueprint('stock_endpoints_v1', __name__)

# USER dump -> serialize / load -> deserialize
@stock_endpoints_v1.route('/info', strict_slashes=False, methods=['GET'])
@requires_auth
@requires_admin
def get_stock_info():
    """-"""
    logging.info('[ROUTER]: Getting stock info')
    try:
        # Getting
        stock_info = StockService.get_stock_info()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    response = StockInfoResponder(user).serialize
    return jsonify(data={
        'last_stockid': stock_info.last_stockid,
        'total_stocks': stock_info.total_stocks
    }), 200
