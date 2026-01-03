from extensions import db

class ProductVariant(db.Model):
    __tablename__ = 'Product_Variants'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    variant_name = db.Column(db.Text, nullable=False)
    variant_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    quantity_unit = db.Column(db.String(55), nullable=True)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product_variant', lazy='dynamic', foreign_keys='CartItem.product_variant_id')
    order_items = db.relationship('OrderItem', backref='product_variant', lazy='dynamic', foreign_keys='OrderItem.product_variant_id')
