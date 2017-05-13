"""Stock Info model"""

from google.appengine.ext import ndb


class StockInfo(ndb.Model):
    """A model representing a Stock Info"""
    # Basic info.
    last_stockid = ndb.IntegerProperty()
    total_stocks = ndb.IntegerProperty(required=True)
    current_price = ndb.FloatProperty(default=50.0)
    last_price = ndb.FloatProperty(default=50.0)

    def __repr__(self):
        return '<StockInfo %r>' % self.last_stockid

    @property
    def id(self):
        return self.key.id()
