from extensions import db

class PromotionProduct(db.Model):
    __tablename__ = 'Promotion_Products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey('Promotions.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
