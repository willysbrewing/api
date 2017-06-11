"""Stock Service"""

import logging
from google.appengine.ext import ndb
from api.models.stock import Stock
from api.models.stock_info import StockInfo
from api.errors import GenericStockError


def get_stock_info():
    logging.info('[SERVICE]: Getting stock info')
    stock_info = StockInfo.query().get()
    return stock_info


def add_stocks(n_stocks):
    logging.info('[SERVICE]: Adding stocks')
    stock_info = StockInfo.query().get()
    if not stock_info:
        stock_info = StockInfo(
            total_stocks=0,
            last_stockid=0
        )
    stock_info.total_stocks += n_stocks
    try:
        stock_info.put()
    except Exception as e:
        raise e
    return stock_info


def get_stock_ids(n_stocks):
    logging.info('[SERVICE]: Modifying StockInfo Pointer')
    if not type(n_stocks) is int:
        raise GenericStockError(message='Stock Info was not modified')
    if n_stocks < 0 or n_stocks > 4:
        raise GenericStockError(message='Invalid Stock number')
    logging.info('[DB]: Transactional')
    stock_info = StockInfo.query().get()
    if stock_info.last_stockid + n_stocks > stock_info.total_stocks:
        raise GenericStockError(message='Number is greater than total_stocks')
    # Generating new stocks
    stocks_ids = range(stock_info.last_stockid+1, stock_info.last_stockid+1+n_stocks)
    try:
        stock_info.last_stockid += n_stocks
        stock_info.put()
    except Exception as e:
        raise e
    return stocks_ids
