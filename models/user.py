from extensions import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(250), nullable=False)
    Last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.BigInteger, nullable=True)
    role = db.Column(db.String(20), nullable=True, default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    addresses = db.relationship('Address', backref='user', lazy='dynamic', foreign_keys='Address.user_id')
    carts = db.relationship('Cart', backref='user', lazy='dynamic', foreign_keys='Cart.user_id')
    orders = db.relationship('Order', backref='user', lazy='dynamic', foreign_keys='Order.user_id')
    coupon_users = db.relationship('CouponUser', backref='user', lazy='dynamic', foreign_keys='CouponUser.user_id')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)