from extensions import db
from datetime import datetime

class Promotion(db.Model):
    __tablename__ = 'Promotions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    promotion_type = db.Column(db.Text, nullable=False)
    discount_type = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    discount_value = db.Column(db.Integer, nullable=False)
    min_order_value = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    promotion_products = db.relationship('PromotionProduct', backref='promotion', lazy='dynamic', foreign_keys='PromotionProduct.promotion_id')
    promotion_categories = db.relationship('PromotionCategory', backref='promotion', lazy='dynamic', foreign_keys='PromotionCategory.promotion_id')
