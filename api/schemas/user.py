"""User Schema"""

from marshmallow import Schema, fields, ValidationError, post_load
from api.models.user import User
from api.schemas.stock import StockSchema

def _validate_gender(gender):
    if gender != 'man' and gender != 'woman' and gender != 'other':
        raise ValidationError('must be a valid value')

def _validate_role(role):
    if role != 'ADMIN' and role != 'USER':
        raise ValidationError('must be a valid role')


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    userid = fields.Integer()
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    gender = fields.Str(validate=_validate_gender)
    address = fields.Str()
    stocks = fields.Nested(StockSchema, many=True)
    news_likes = fields.List(fields.Integer)
    events_going = fields.List(fields.Integer)
    contests_applied = fields.List(fields.Integer)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(validate=_validate_role)


    @post_load
    def make_user(self, data):
        return User(**data)
