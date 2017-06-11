"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import requires_auth, requires_admin, validate_new_stocks
from api.services import stock_service as StockService
from api.responders import StockInfoResponder

stock_endpoints_v1 = Blueprint('stock_endpoints_v1', __name__)


@stock_endpoints_v1.route('/add', strict_slashes=False, methods=['POST'])
@requires_auth
@requires_admin
@validate_new_stocks
def add_stocks(n_stocks):
    """-"""
    logging.info('[ROUTER]: Init or modify stock info')
    try:
        # Getting
        stock_info = StockService.add_stocks(n_stocks)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize, schema is not required
    response = StockInfoResponder({
        'last_stockid': stock_info.last_stockid,
        'total_stocks': stock_info.total_stocks
    }).serialize
    return jsonify(data=response), 200


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
    # Serialize, schema is not required
    if stock_info:
        response = StockInfoResponder({
            'last_stockid': stock_info.last_stockid,
            'total_stocks': stock_info.total_stocks
        }).serialize
    else:
        response = stock_info
    return jsonify(data=response), 200
