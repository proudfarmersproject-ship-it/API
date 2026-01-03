from extensions import db

class PromotionCategory(db.Model):
    __tablename__ = 'Promotion_Categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey('Promotions.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
