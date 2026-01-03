from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'Products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
    is_active = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stock_quantity = db.Column(db.Integer, default=0)
    stock_unit = db.Column(db.Enum('Kg', 'gm', 'L', 'ml', 'other', name='stock_unit_enum'), default='other')
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', foreign_keys='ProductImage.product_id')
    variants = db.relationship('ProductVariant', backref='product', lazy='dynamic', foreign_keys='ProductVariant.product_id')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic', foreign_keys='OrderItem.product_id')
    promotion_products = db.relationship('PromotionProduct', backref='product', lazy='dynamic', foreign_keys='PromotionProduct.product_id')
