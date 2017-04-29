"""User Schema"""

from marshmallow import Schema, fields, ValidationError, post_dump


def _validate_gender(gender):
    if gender != 'male' and gender != 'female':
        raise ValidationError('must be a valid value')


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    gender = fields.Str(validate=_validate_gender)
    address = fields.Str()
    created_at = fields.DateTime(dump_only=True)
