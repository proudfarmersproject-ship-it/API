from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
import os
import pymysql

# Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database configuration
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '40377')
DB_NAME = os.getenv('DB_NAME', 'railway')

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize extensions
from extensions import db, bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Initialize API
api = Api(app)

# Import all models
from models import *

# Import resources
from resources.users.user_resource import UserListResource, UserResource, LoginResource
from resources.users.address_resource import AddressListResource, AddressResource
from resources.product.category_resource import CategoryListResource, CategoryResource
from resources.product.product_resource import ProductListResource, ProductResource
from resources.product.product_image_resource import ProductImageListResource, ProductImageResource
from resources.product.product_variant_resource import ProductVariantListResource, ProductVariantResource
from resources.product.products_complete import ( ProductCompleteListResource,
    ProductCompleteResource,
    ProductCreateCompleteResource,
    ProductUploadImagesResource,
    ProductImageDeleteResource,
    ProductUpdateResource,
    ProductAddVariantsResource)
from resources.cart.cart_resource import CartListResource, CartResource
from resources.cart.cart_item_resource import CartItemListResource, CartItemResource
from resources.cart.crat_per_user_with_items import CartResourceAdvanced
from resources.cart.coupon_resource import CouponListResource, CouponResource
from resources.orders.order_resource import OrderListResource, OrderResource
from resources.orders.order_item_resource import OrderItemListResource, OrderItemResource
from resources.promotion_resource import PromotionListResource, PromotionResource

# Register API endpoints
# Users
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserResource, '/api/users/<int:id>')
api.add_resource(LoginResource, '/api/login')

# Addresses
api.add_resource(AddressListResource, '/api/addresses')
api.add_resource(AddressResource, '/api/addresses/<int:id>')

# Categories
api.add_resource(CategoryListResource, '/api/categories')
api.add_resource(CategoryResource, '/api/categories/<int:id>')

# Products
api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:id>')

#from product_complete import resources
api.add_resource(ProductCompleteListResource, '/api/products')
api.add_resource(ProductCompleteResource, '/api/products/<int:product_id>')
api.add_resource(ProductCreateCompleteResource, '/api/products/create')
api.add_resource(ProductUpdateResource, '/api/products/<int:product_id>/update')
api.add_resource(ProductUploadImagesResource, '/api/products/<int:product_id>/images')
api.add_resource(ProductImageDeleteResource, '/api/images/<int:image_id>')
api.add_resource(ProductAddVariantsResource, '/api/products/<int:product_id>/variants')

# Product Images
api.add_resource(ProductImageListResource, '/api/product-images')
api.add_resource(ProductImageResource, '/api/product-images/<int:id>')

# Product Variants
api.add_resource(ProductVariantListResource, '/api/product-variants')
api.add_resource(ProductVariantResource, '/api/product-variants/<int:id>')

# Carts
api.add_resource(CartListResource, '/api/carts')
api.add_resource(CartResource, '/api/carts/<int:id>')

api.add_resource(CartResourceAdvanced, '/api/user/<int:user_id>/carts')

# Cart Items
api.add_resource(CartItemListResource, '/api/cart-items')
api.add_resource(CartItemResource, '/api/cart-items/<int:id>')

# Coupons
api.add_resource(CouponListResource, '/api/coupons')
api.add_resource(CouponResource, '/api/coupons/<int:id>')

# Orders
api.add_resource(OrderListResource, '/api/orders')
api.add_resource(OrderResource, '/api/orders/<int:id>')

# Order Items
api.add_resource(OrderItemListResource, '/api/order-items')
api.add_resource(OrderItemResource, '/api/order-items/<int:id>')

# Promotions
api.add_resource(PromotionListResource, '/api/promotions')
api.add_resource(PromotionResource, '/api/promotions/<int:id>')

@app.route('/')
def home():
    return '<h1>Welcome to E-commerce API</h1><p>Visit /api/* endpoints for API access</p>'

if __name__ == '__main__':
    print(f"Connecting to: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    print("Initializing Backblaze B2 Storage...")

    
    with app.app_context():
        try:
            # Test connection
            db.engine.connect()
            print("✓ Database connection successful!")
            
            # Create tables (only if they don't exist)
            db.create_all()
            print("✓ Database tables ready!")

            try:
                from utils.b2_storage import get_b2_storage
                storage =  get_b2_storage()
                print("✓ Backblaze B2 storage initialized!")
                print(f" Bucket: {storage.bucket_name}")
            except Exception as e:
                print(f"⚠ Warning: B2 Storage initialization failed: {e}")
                print("  Products will work but image upload will fail")
            
        except Exception as e:
            print(f"✗ Database error: {e}")
            exit(1)
            
    print("\n🚀 Server starting on http://localhost:5000")
    app.run()