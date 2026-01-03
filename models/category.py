from extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'Categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic', foreign_keys='Product.category_id')
    promotion_categories = db.relationship('PromotionCategory', backref='category', lazy='dynamic', foreign_keys='PromotionCategory.category_id')