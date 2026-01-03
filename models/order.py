from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'Orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('Addresses.id'), nullable=False)
    actual_amount = db.Column(db.DECIMAL(10, 0), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'paid', 'failed', name='payment_status_enum'), default='pending')
    order_status = db.Column(db.Enum('pending', 'confirmed', 'out_for_Delivery', 'delivered', 'cancelled', name='order_status_enum'), default='pending')
    stripe_payment_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    discount_source = db.Column(db.String(50), nullable=True)
    discount_amount = db.Column(db.DECIMAL(10, 0), default=0)
    sub_total = db.Column(db.DECIMAL(10, 0), nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic', foreign_keys='OrderItem.order_id')

