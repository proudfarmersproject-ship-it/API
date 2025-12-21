from .auth import auth_bp
from .products import products_bp
from .categories import categories_bp
from .cart import cart_bp
from .orders import orders_bp
from .addresses import addresses_bp
from .coupons import coupons_bp
from .admin import admin_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
    app.register_blueprint(addresses_bp, url_prefix="/api/addresses")
    app.register_blueprint(coupons_bp, url_prefix="/api/coupons")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
