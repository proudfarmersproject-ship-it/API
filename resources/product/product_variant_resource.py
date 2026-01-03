from flask_restful import Resource, reqparse, fields, marshal_with
from models.product_variant import ProductVariant
from extensions import db

product_variant_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'variant_name': fields.String,
    'variant_price': fields.Float,
    'stock_quantity': fields.Integer,
    'quantity_unit': fields.String
}

product_variant_parser = reqparse.RequestParser()
product_variant_parser.add_argument('product_id', type=int, required=True)
product_variant_parser.add_argument('variant_name', type=str, required=True)
product_variant_parser.add_argument('variant_price', type=float, required=True)
product_variant_parser.add_argument('stock_quantity', type=int)
product_variant_parser.add_argument('quantity_unit', type=str)

class ProductVariantListResource(Resource):
    @marshal_with(product_variant_fields)
    def get(self):
        variants = ProductVariant.query.all()
        return variants
    
    @marshal_with(product_variant_fields)
    def post(self):
        args = product_variant_parser.parse_args()
        variant = ProductVariant(**args)
        db.session.add(variant)
        db.session.commit()
        return variant, 201

class ProductVariantResource(Resource):
    @marshal_with(product_variant_fields)
    def get(self, id):
        variant = ProductVariant.query.get_or_404(id)
        return variant
    
    @marshal_with(product_variant_fields)
    def patch(self, id):
        args = product_variant_parser.parse_args()
        variant = ProductVariant.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(variant, key, value)
        db.session.commit()
        return variant
    
    def delete(self, id):
        variant = ProductVariant.query.get_or_404(id)
        db.session.delete(variant)
        db.session.commit()
        return {'message': 'Product variant deleted'}, 204