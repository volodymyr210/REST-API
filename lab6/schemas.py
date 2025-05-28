from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    year = fields.Integer(required=True)
