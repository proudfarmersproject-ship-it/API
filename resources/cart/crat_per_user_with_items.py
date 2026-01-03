from flask_restful import Resource, reqparse, fields, marshal_with, marshal, abort
from models.cart import Cart
from models.product_variant import ProductVariant
from models.cart_item import CartItem
from models.user import User
from extensions import db
from sqlalchemy.orm import joinedload

cart_item_nested_fields = {
    'id': fields.Integer,
    'cart_id': fields.Integer,
    'product_variant_id': fields.Integer,
    'quantity': fields.Integer,
    'product_actual_price': fields.Float,
    'applicable_promotion_id': fields.Integer,
    'promotion_discount': fields.Float,
    'After_discounted_total': fields.Float,
    'updated_at': fields.DateTime,
    # Add product variant details
    'product_variant': fields.Nested({
        'id': fields.Integer,
        'variant_name': fields.String,
        'variant_price': fields.Float,
        'product': fields.Nested({
            'id': fields.Integer,
            'name': fields.String,
            'description': fields.String
        })
    })
}

cart_detail_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'coupon_active': fields.Integer,
    'coupon_id': fields.Integer,
    'coupon_code': fields.String,
    'coupon_discount': fields.Float,
    'dicounted_total_price': fields.Float,
    'actual_amount': fields.Float,
    'updated_at': fields.DateTime,
    # Nested cart items
    'cart_items': fields.List(fields.Nested(cart_item_nested_fields)),
    # User details
    'user': fields.Nested({
        'id': fields.Integer,
        'First_name': fields.String,
        'Last_name': fields.String,
        'email': fields.String
    })
}

# Parser for cart updates
cart_update_parser = reqparse.RequestParser()
cart_update_parser.add_argument('coupon_active', type=int, choices=[0, 1])
cart_update_parser.add_argument('coupon_id', type=int)
cart_update_parser.add_argument('coupon_code', type=str)
cart_update_parser.add_argument('coupon_discount', type=float)
cart_update_parser.add_argument('dicounted_total_price', type=float)
cart_update_parser.add_argument('actual_amount', type=float )

class CartResourceAdvanced(Resource):
    def get(self, user_id):
        """
        Get cart with all items and product details by user_id
        """
               
        cart = Cart.query.options(
            joinedload(Cart.user),
            joinedload(Cart.cart_items).joinedload(CartItem.product_variant).joinedload(ProductVariant.product)
        ).filter_by(user_id=user_id).first()
        
        if not cart:
            abort(404, message=f"Cart for user_id {user_id} not found")
        
        return {
            'success': True,
            'cart': marshal(cart, cart_detail_fields)
        }, 200
    def post(self,user_id):
        """create new cart for user with user_id"""
        #check if user exists 
        user = User.query.get(user_id)
        if not user:
            abort(404, message=f"User with id {user_id} not found")
        # Check if cart already exists for this user
        existing_cart = Cart.query.filter_by(user_id=user_id).first()
        if existing_cart:
            abort(400, message=f"Cart already exists for user_id {user_id}")
        args = cart_update_parser.parse_args()
        cart = Cart(
            user_id=user_id,
            coupon_active=args.get('coupon_active', 0),
            coupon_id=args.get('coupon_id'),
            coupon_code=args.get('coupon_code'),
            coupon_discount=args.get('coupon_discount', 0.0),
            dicounted_total_price=args.get('dicounted_total_price', 0.0),
            actual_amount=args.get('actual_amount', 0.0))
        db.session.add(cart)
        db.session.commit()
        cart = Cart.query.options(joinedload(Cart.user), joinedload(Cart.cart_items)).filter_by(id=cart.id).first()
        return {
            'success': True,
            'cart': marshal(cart, cart_detail_fields)
        }, 201
    def patch(self, user_id):
         """Update cart details by user_id"""
         cart = Cart.query.filter_by(user_id=user_id).first()
         if not cart:
             abort(404, message=f"Cart for user_id {user_id} not found") 
         args = cart_update_parser.parse_args()
         # Update only provided fields
         for key, value in args.items():
             if value is not None:
                 setattr(cart, key, value)
         db.session.commit()
         cart = Cart.query.options(
             joinedload(cart.user),
             joinedload(cart.cart_items).joinedload(CartItem.product_variant).joinedload(ProductVariant.product)
         ).filter_by(user_id=user_id).first()
         return {
             'success': True,
             'cart': marshal(cart, cart_detail_fields)
         }, 200
    def delete(self, user_id):
        """
        Delete cart and all associated cart items by user_id
        """
        cart = Cart.query.filter_by(user_id=user_id).first()
        
        if not cart:
            abort(404, message=f"Cart for user_id {user_id} not found")
        
        # Delete associated cart items first
        CartItem.query.filter_by(cart_id=cart.id).delete()
        
        # Delete the cart
        db.session.delete(cart)
        db.session.commit()
        
        return {
            'success': True,
            'message': f'Cart for user_id {user_id} deleted successfully'
        }, 200
 