"""Event model"""

from google.appengine.ext import ndb


class Event(ndb.Model):
    """A model representing a Event"""
    # Basic info.
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    going = ndb.IntegerProperty(repeated=True)
    link_url = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty(required=True)

    def __repr__(self):
        return '<Event %r>' % self.title

    @property
    def id(self):
        return self.key.id()
