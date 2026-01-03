from flask_restful import Resource, reqparse, fields, marshal_with
from models.cart import Cart
from extensions import db

cart_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'coupon_active': fields.Integer,
    'coupon_id': fields.Integer,
    'coupon_code': fields.String,
    'coupon_discount': fields.Float,
    'dicounted_total_price': fields.Float,
    'actual_amount': fields.Float,
    'updated_at': fields.DateTime
}

cart_parser = reqparse.RequestParser()
cart_parser.add_argument('user_id', type=int, required=True)
cart_parser.add_argument('coupon_active', type=int, choices=[0, 1])
cart_parser.add_argument('coupon_id', type=int)
cart_parser.add_argument('coupon_code', type=str)
cart_parser.add_argument('coupon_discount', type=float)
cart_parser.add_argument('dicounted_total_price', type=float)
cart_parser.add_argument('actual_amount', type=float)

class CartListResource(Resource):
    @marshal_with(cart_fields)
    def get(self):
        carts = Cart.query.all()
        return carts
    
    @marshal_with(cart_fields)
    def post(self):
        args = cart_parser.parse_args()
        cart = Cart(**args)
        db.session.add(cart)
        db.session.commit()
        return cart, 201

class CartResource(Resource):
    @marshal_with(cart_fields)
    def get(self, id):
        cart = Cart.query.get_or_404(id)
        return cart
    
    @marshal_with(cart_fields)
    def patch(self, id):
        args = cart_parser.parse_args()
        cart = Cart.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(cart, key, value)
        db.session.commit()
        return cart
    
    def delete(self, id):
        cart = Cart.query.get_or_404(id)
        db.session.delete(cart)
        db.session.commit()
        return {'message': 'Cart deleted'}, 204
