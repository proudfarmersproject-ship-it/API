from extensions import db

class OrderItem(db.Model):
    __tablename__ = 'Order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    product_variant_id = db.Column(db.Integer, db.ForeignKey('Product_Variants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL(10, 0), nullable=False)