"""News Schema"""

from marshmallow import Schema, fields, post_load
from api.models.news import News


class NewsSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    likes = fields.List(fields.Integer)
    image_url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)


    @post_load
    def make_news(self, data):
        return News(**data)
