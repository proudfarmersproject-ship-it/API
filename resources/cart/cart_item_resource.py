from flask_restful import Resource, reqparse, fields, marshal_with
from models.cart_item import CartItem
from extensions import db

cart_item_fields = {
    'id': fields.Integer,
    'cart_id': fields.Integer,
    'product_variant_id': fields.Integer,
    'quantity': fields.Integer,
    'product_actual_price': fields.Float,
    'applicable_promotion_id': fields.Integer,
    'promotion_discount': fields.Float,
    'After_discounted_total': fields.Float,
    'updated_at': fields.DateTime
}

cart_item_parser = reqparse.RequestParser()
cart_item_parser.add_argument('cart_id', type=int, required=True)
cart_item_parser.add_argument('product_variant_id', type=int, required=True)
cart_item_parser.add_argument('quantity', type=int, required=True)
cart_item_parser.add_argument('product_actual_price', type=float, required=True)
cart_item_parser.add_argument('applicable_promotion_id', type=int)
cart_item_parser.add_argument('promotion_discount', type=float)
cart_item_parser.add_argument('After_discounted_total', type=float)

class CartItemListResource(Resource):
    @marshal_with(cart_item_fields)
    def get(self):
        items = CartItem.query.all()
        return items
    
    @marshal_with(cart_item_fields)
    def post(self):
        args = cart_item_parser.parse_args()
        item = CartItem(**args)
        db.session.add(item)
        db.session.commit()
        return item, 201

class CartItemResource(Resource):
    @marshal_with(cart_item_fields)
    def get(self, id):
        item = CartItem.query.get_or_404(id)
        return item
    
    @marshal_with(cart_item_fields)
    def patch(self, id):
        args = cart_item_parser.parse_args()
        item = CartItem.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(item, key, value)
        db.session.commit()
        return item
    
    def delete(self, id):
        item = CartItem.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Cart item deleted'}, 204
