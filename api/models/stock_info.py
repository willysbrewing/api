"""Stock Info model"""

from google.appengine.ext import ndb


class StockInfo(ndb.Model):
    """A model representing a Stock Info"""
    # Basic info.
    last_stockid = ndb.IntegerProperty(required=True)
    total_stocks = ndb.IntegerProperty(required=True)

    def __repr__(self):
        return '<StockInfo %r>' % self.last_stockid

    @property
    def id(self):
        return self.key.id()
