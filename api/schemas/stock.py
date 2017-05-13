"""Stock Schema"""

from marshmallow import Schema, fields
from api.models.stock import Stock


class StockSchema(Schema):
    stockid = fields.Integer(dump_only=True)
