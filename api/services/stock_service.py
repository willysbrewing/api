"""Stock Service"""

import logging
from google.appengine.ext import ndb
from api.models.stock import Stock
from api.models.stock_info import StockInfo


def get_stock_info():
    logging.info('[SERVICE]: Getting stock info')
    stock_info = StockInfo.query(use_cache=True, use_memcache=True)
    if not stock_info:
        raise Exception(message='Not stock info')
    return stock_info
