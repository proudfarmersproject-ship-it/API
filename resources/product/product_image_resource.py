from flask_restful import Resource, reqparse, fields, marshal_with
from models.product_image import ProductImage
from extensions import db

product_image_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'image_path': fields.String,
    'alt_text': fields.String,
    'is_primary': fields.Integer
}

product_image_parser = reqparse.RequestParser()
product_image_parser.add_argument('product_id', type=int, required=True)
product_image_parser.add_argument('image_path', type=str, required=True)
product_image_parser.add_argument('alt_text', type=str)
product_image_parser.add_argument('is_primary', type=int, choices=[0, 1])

class ProductImageListResource(Resource):
    @marshal_with(product_image_fields)
    def get(self):
        images = ProductImage.query.all()
        return images
    
    @marshal_with(product_image_fields)
    def post(self):
        args = product_image_parser.parse_args()
        image = ProductImage(**args)
        db.session.add(image)
        db.session.commit()
        return image, 201

class ProductImageResource(Resource):
    @marshal_with(product_image_fields)
    def get(self, id):
        image = ProductImage.query.get_or_404(id)
        return image
    
    @marshal_with(product_image_fields)
    def patch(self, id):
        args = product_image_parser.parse_args()
        image = ProductImage.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(image, key, value)
        db.session.commit()
        return image
    
    def delete(self, id):
        image = ProductImage.query.get_or_404(id)
        db.session.delete(image)
        db.session.commit()
        return {'message': 'Product image deleted'}, 204