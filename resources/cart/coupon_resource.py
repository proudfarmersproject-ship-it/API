from flask_restful import Resource, reqparse, fields, marshal_with
from models.coupon import Coupon
from extensions import db
from datetime import datetime

coupon_fields = {
    'id': fields.Integer,
    'code': fields.String,
    'discount_type': fields.String,
    'discount_values': fields.Integer,
    'min_order_value': fields.Integer,
    'usage_limit': fields.Integer,
    'used_count': fields.Integer,
    'start_date': fields.DateTime,
    'end_date': fields.DateTime,
    'is_ative': fields.Integer
}

coupon_parser = reqparse.RequestParser()
coupon_parser.add_argument('code', type=str, required=True)
coupon_parser.add_argument('discount_type', type=str, required=True)
coupon_parser.add_argument('discount_values', type=int, required=True)
coupon_parser.add_argument('min_order_value', type=int)
coupon_parser.add_argument('usage_limit', type=int)
coupon_parser.add_argument('start_date', type=str, required=True)
coupon_parser.add_argument('end_date', type=str, required=True)
coupon_parser.add_argument('is_ative', type=int, choices=[0, 1])

class CouponListResource(Resource):
    @marshal_with(coupon_fields)
    def get(self):
        coupons = Coupon.query.all()
        return coupons
    
    @marshal_with(coupon_fields)
    def post(self):
        args = coupon_parser.parse_args()
        args['start_date'] = datetime.fromisoformat(args['start_date'])
        args['end_date'] = datetime.fromisoformat(args['end_date'])
        coupon = Coupon(**args)
        db.session.add(coupon)
        db.session.commit()
        return coupon, 201

class CouponResource(Resource):
    @marshal_with(coupon_fields)
    def get(self, id):
        coupon = Coupon.query.get_or_404(id)
        return coupon
    
    @marshal_with(coupon_fields)
    def patch(self, id):
        args = coupon_parser.parse_args()
        if args.get('start_date'):
            args['start_date'] = datetime.fromisoformat(args['start_date'])
        if args.get('end_date'):
            args['end_date'] = datetime.fromisoformat(args['end_date'])
        coupon = Coupon.query.get_or_404(id)
        for key, value in args.items():
            if value is not None:
                setattr(coupon, key, value)
        db.session.commit()
        return coupon
    
    def delete(self, id):
        coupon = Coupon.query.get_or_404(id)
        db.session.delete(coupon)
        db.session.commit()
        return {'message': 'Coupon deleted'}, 204
