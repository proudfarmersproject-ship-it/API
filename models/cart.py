from extensions import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'Carts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    coupon_active = db.Column(db.Integer, default=0)
    coupon_id = db.Column(db.Integer, db.ForeignKey('Coupons.id'), nullable=True)
    coupon_code = db.Column(db.Text, nullable=True)
    coupon_discount = db.Column(db.DECIMAL(10, 2), default=0)
    dicounted_total_price = db.Column(db.DECIMAL(10, 0), default=0)
    actual_amount = db.Column(db.DECIMAL(10, 0), default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    coupon = db.relationship('Coupon', backref='carts', foreign_keys=[coupon_id])
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic', foreign_keys='CartItem.cart_id')
