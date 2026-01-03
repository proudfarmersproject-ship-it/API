from flask_restful import Resource, reqparse, fields, marshal_with
from models.order_item import OrderItem
from extensions import db

order_item_fields = {
    'id': fields.Integer,
    'order_id': fields.Integer,
    'product_id': fields.Integer,
    'product_variant_id': fields.Integer,
    'quantity': fields.Integer,
    'price': fields.Float
}

order_item_parser = reqparse.RequestParser()
order_item_parser.add_argument('order_id', type=int, required=True)
order_item_parser.add_argument('product_id', type=int, required=True)
order_item_parser.add_argument('product_variant_id', type=int, required=True)
order_item_parser.add_argument('quantity', type=int, required=True)
order_item_parser.add_argument('price', type=float, required=True)

class OrderItemListResource(Resource):
    @marshal_with(order_item_fields)
    def get(self):
        items = OrderItem.query.all()
        return items
    
    @marshal_with(order_item_fields)
    def post(self):
        args = order_item_parser.parse_args()
        item = OrderItem(**args)
        db.session.add(item)
        db.session.commit()
        return item, 201

class OrderItemResource(Resource):
    @marshal_with(order_item_fields)
    def get(self, id):
        item = OrderItem.query.get_or_404(id)
        return item
    
    @marshal_with(order_item_fields)
    def patch(self, id):
        args = order_item_parser.parse_args()
        item = OrderItem.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(item, key, value)
        db.session.commit()
        return item
    
    def delete(self, id):
        item = OrderItem.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Order item deleted'}, 204
