"""User Schema"""

from marshmallow import Schema, fields, ValidationError, post_load
from api.models import User

def _validate_gender(gender):
    if gender != 'man' and gender != 'woman' and gender != 'other':
        raise ValidationError('must be a valid value')


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    userid = fields.Integer()
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    gender = fields.Str(validate=_validate_gender)
    address = fields.Str()
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data):
        return User(**data)
