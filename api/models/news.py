"""News model"""

from google.appengine.ext import ndb


class News(ndb.Model):
    """A model representing a News"""
    # Basic info.
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    likes = ndb.IntegerProperty(repeated=True)
    image_url = ndb.StringProperty(required=True)

    def __repr__(self):
        return '<News %r>' % self.title

    @property
    def id(self):
        return self.key.id()
