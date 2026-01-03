from extensions import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'Carts_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('Carts.id'), nullable=False)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('Product_Variants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product_actual_price = db.Column(db.DECIMAL(10, 0), nullable=False)
    applicable_promotion_id = db.Column(db.Integer, db.ForeignKey('Promotions.id'), nullable=True)
    promotion_discount = db.Column(db.DECIMAL(10, 2), default=0)
    After_discounted_total = db.Column(db.DECIMAL(10, 0), default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    promotion = db.relationship('Promotion', backref='cart_items', foreign_keys=[applicable_promotion_id])
