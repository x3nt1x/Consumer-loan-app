from app.models.client import Client
from marshmallow import Schema, fields, post_load, validate


class ClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=64))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=64))
    personal_id = fields.Integer(required=True)

    @post_load
    def make_object(self, data):
        return Client(**data)


client_schema = ClientSchema()
