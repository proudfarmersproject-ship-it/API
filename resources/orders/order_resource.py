from flask_restful import Resource, reqparse, fields, marshal_with
from models.order import Order
from extensions import db

order_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'address_id': fields.Integer,
    'actual_amount': fields.Float,
    'payment_status': fields.String,
    'order_status': fields.String,
    'stripe_payment_id': fields.Integer,
    'created_at': fields.DateTime,
    'discount_source': fields.String,
    'discount_amount': fields.Float,
    'sub_total': fields.Float
}

order_parser = reqparse.RequestParser()
order_parser.add_argument('user_id', type=int, required=True)
order_parser.add_argument('address_id', type=int, required=True)
order_parser.add_argument('actual_amount', type=float, required=True)
order_parser.add_argument('payment_status', type=str)
order_parser.add_argument('order_status', type=str)
order_parser.add_argument('stripe_payment_id', type=int)
order_parser.add_argument('discount_source', type=str)
order_parser.add_argument('discount_amount', type=float)
order_parser.add_argument('sub_total', type=float, required=True)

class OrderListResource(Resource):
    @marshal_with(order_fields)
    def get(self):
        orders = Order.query.all()
        return orders
    
    @marshal_with(order_fields)
    def post(self):
        args = order_parser.parse_args()
        order = Order(**args)
        db.session.add(order)
        db.session.commit()
        return order, 201

class OrderResource(Resource):
    @marshal_with(order_fields)
    def get(self, id):
        order = Order.query.get_or_404(id)
        return order
    
    @marshal_with(order_fields)
    def patch(self, id):
        args = order_parser.parse_args()
        order = Order.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(order, key, value)
        db.session.commit()
        return order
    
    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted'}, 204
