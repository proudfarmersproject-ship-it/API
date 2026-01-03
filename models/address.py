from extensions import db

class Address(db.Model):
    __tablename__ = 'Addresses'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    full_name = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address_line1 = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(45), nullable=False)
    pincode = db.Column(db.String(45), nullable=False)
    is_default = db.Column(db.Integer, default=0)
    
    # Relationships
    orders = db.relationship('Order', backref='address', lazy='dynamic', foreign_keys='Order.address_id')