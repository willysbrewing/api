"""Stock model"""

from google.appengine.ext import ndb


class Stock(ndb.Model):
    """A model representing a Stock"""
    # Basic info.
    stockid = ndb.IntegerProperty(required=True)

    def __repr__(self):
        return '<Stock %r>' % self.stockid

    @property
    def id(self):
        return self.key.id()
