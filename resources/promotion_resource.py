from flask_restful import Resource, reqparse, fields, marshal_with
from models.promotion import Promotion
from extensions import db
from datetime import datetime

promotion_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'promotion_type': fields.String,
    'discount_type': fields.String,
    'description': fields.String,
    'discount_value': fields.Integer,
    'min_order_value': fields.Integer,
    'active': fields.Integer,
    'created_at': fields.DateTime,
    'start_date': fields.DateTime,
    'end_date': fields.DateTime
}

promotion_parser = reqparse.RequestParser()
promotion_parser.add_argument('title', type=str, required=True)
promotion_parser.add_argument('promotion_type', type=str, required=True,choices=['product', 'category'])
promotion_parser.add_argument('discount_type', type=str, required=True)
promotion_parser.add_argument('description', type=str)
promotion_parser.add_argument('discount_value', type=int, required=True)
promotion_parser.add_argument('min_order_value', type=int)
promotion_parser.add_argument('active', type=int, choices=[0, 1])
promotion_parser.add_argument('start_date', type=str, required=True)
promotion_parser.add_argument('end_date', type=str, required=True)

class PromotionListResource(Resource):
    @marshal_with(promotion_fields)
    def get(self):
        promotions = Promotion.query.all()
        return promotions
    
    @marshal_with(promotion_fields)
    def post(self):
        args = promotion_parser.parse_args()
        args['start_date'] = datetime.fromisoformat(args['start_date'])
        args['end_date'] = datetime.fromisoformat(args['end_date'])
        promotion = Promotion(**args)
        db.session.add(promotion)
        db.session.commit()
        return promotion, 201

class PromotionResource(Resource):
    @marshal_with(promotion_fields)
    def get(self, id):
        promotion = Promotion.query.get_or_404(id)
        return promotion
    
    @marshal_with(promotion_fields)
    def patch(self, id):
        args = promotion_parser.parse_args()
        if args.get('start_date'):
            args['start_date'] = datetime.fromisoformat(args['start_date'])
        if args.get('end_date'):
            args['end_date'] = datetime.fromisoformat(args['end_date'])
        promotion = Promotion.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(promotion, key, value)
        db.session.commit()
        return promotion
    
    def delete(self, id):
        promotion = Promotion.query.get_or_404(id)
        db.session.delete(promotion)
        db.session.commit()
        return {'message': 'Promotion deleted'}, 204
