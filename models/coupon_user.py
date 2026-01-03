from extensions import db

class CouponUser(db.Model):
    __tablename__ = 'Coupon_Code_Users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('Coupons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)