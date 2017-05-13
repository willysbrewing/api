"""User model"""

from api.models.stock import Stock

from google.appengine.ext import ndb


class User(ndb.Model):
    """A model representing a User"""
    # Basic info.
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    gender = ndb.StringProperty(
        choices=('male', 'female', 'other')
    )
    address = ndb.StringProperty()
    mobile_number = ndb.StringProperty()
    stocks = ndb.StructuredProperty(Stock, repeated=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    role = ndb.StringProperty(
        choices=('ADMIN', 'USER'),
        default='USER'
    )
    news_likes = ndb.IntegerProperty(repeated=True)
    events_going = ndb.IntegerProperty(repeated=True)
    contests_applied = ndb.IntegerProperty(repeated=True)


    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def id(self):
        return self.key.id()
