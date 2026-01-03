from extensions import db
from datetime import datetime

class Coupon(db.Model):
    __tablename__ = 'Coupons'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Text, nullable=False, unique=True)
    discount_type = db.Column(db.String(10), nullable=False)
    discount_values = db.Column(db.Integer, nullable=False)
    min_order_value = db.Column(db.Integer, default=0)
    usage_limit = db.Column(db.Integer, nullable=True)
    used_count = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Integer, default=1)
    
    # Relationships
    coupon_users = db.relationship('CouponUser', backref='coupon', lazy='dynamic', foreign_keys='CouponUser.coupon_id')
