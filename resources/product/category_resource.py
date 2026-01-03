from flask_restful import Resource, reqparse, fields, marshal_with
from models.category import Category
from extensions import db

category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime
}

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, required=True)
category_parser.add_argument('description', type=str)

class CategoryListResource(Resource):
    @marshal_with(category_fields)
    def get(self):
        categories = Category.query.all()
        return categories
    
    @marshal_with(category_fields)
    def post(self):
        args = category_parser.parse_args()
        category = Category(**args)
        db.session.add(category)
        db.session.commit()
        return category, 201

class CategoryResource(Resource):
    @marshal_with(category_fields)
    def get(self, id):
        category = Category.query.get_or_404(id)
        return category
    
    @marshal_with(category_fields)
    def patch(self, id):
        args = category_parser.parse_args()
        category = Category.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(category, key, value)
        db.session.commit()
        return category
    
    def delete(self, id):
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted'}, 204