from marshmallow import Schema, fields, post_load
from .model import Car, Order, User
from flask_bcrypt import Bcrypt


class CarSchema(Schema):
    id = fields.Int(required=True)
    model = fields.Str(required=True)
    status = fields.Str(validate=lambda x: x in ['new', 'old', 'used'], required=True)

    @post_load
    def make_car(self, data, **kwargs):
        return Car(**data)


class OrderSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    car_id = fields.Int(required=True)
    price = fields.Int(required=True)
    status = fields.Str(validate=lambda x: x in ['accepted', 'denied', 'unprocessed'], required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)

    @post_load
    def make_order(self, data,**kwargs):
        return Order(**data)


class UserSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(validate=lambda email: '@' and '.' in email, required=True)
    password = fields.Function(deserialize=lambda obj: Bcrypt().generate_password_hash(obj), load_only=True)


    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
