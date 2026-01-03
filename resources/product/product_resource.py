from flask_restful import Resource, reqparse, fields, marshal_with
from models.product import Product
from extensions import db

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'category_id': fields.Integer,
    'is_active': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'stock_quantity': fields.Integer,
    'stock_unit': fields.String
}

product_parser = reqparse.RequestParser()
product_parser.add_argument('name', type=str, required=True)
product_parser.add_argument('description', type=str)
product_parser.add_argument('category_id', type=int, required=True)
product_parser.add_argument('is_active', type=int, choices=[0, 1])
product_parser.add_argument('stock_quantity', type=int)
product_parser.add_argument('stock_unit', type=str, choices=['Kg', 'gm', 'L', 'ml', 'other'])

class ProductListResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        products = Product.query.all()
        return products
    
    @marshal_with(product_fields)
    def post(self):
        args = product_parser.parse_args()
        product = Product(**args)
        db.session.add(product)
        db.session.commit()
        return product, 201

class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self, id):
        product = Product.query.get_or_404(id)
        return product
    
    @marshal_with(product_fields)
    def patch(self, id):
        args = product_parser.parse_args()
        product = Product.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(product, key, value)
        db.session.commit()
        return product
    
    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}, 204