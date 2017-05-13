"""News Schema"""

from marshmallow import Schema, fields, post_load
from api.models.event import Event


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    going = fields.Integer()
    image_url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)


    @post_load
    def make_news(self, data):
        return News(**data)
