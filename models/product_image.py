from extensions import db

class ProductImage(db.Model):
    __tablename__ = 'Product_Images'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    alt_text = db.Column(db.Text, nullable=True)
    is_primary = db.Column(db.Integer, default=0)