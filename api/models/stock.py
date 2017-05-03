"""Stock model"""

from google.appengine.ext import ndb


class Stock(ndb.Model):
    """A model representing a Stock"""
    # Basic info.
    stockid = ndb.IntegerProperty(required=True)
    current_price = ndb.FloatProperty(default=50.0)
    last_price = ndb.FloatProperty(default=50.0)

    def __repr__(self):
        return '<Stock %r>' % self.stockid

    @property
    def id(self):
        return self.key.id()
