from flask import request
from flask_restful import Resource, reqparse, fields, marshal, abort
from models.product import Product
from models.product_image import ProductImage
from models.product_variant import ProductVariant
from models.category import Category
from extensions import db
from sqlalchemy.orm import joinedload
from datetime import datetime
from werkzeug.exceptions import HTTPException

# Import B2 storage
from utils.b2_storage import get_b2_storage

# Custom field to convert image_path to full URL
class ImageUrlField(fields.Raw):
    def format(self, value):
        if value:
            try:
                storage = get_b2_storage()
                return storage.get_file_url(value)
            except:
                return None
        return None

# Field definitions
category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

product_image_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'image_path': fields.String,
    'image_url': ImageUrlField(attribute='image_path'),
    'alt_text': fields.String,
    'is_primary': fields.Integer
}

product_variant_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'variant_name': fields.String,
    'variant_price': fields.Float,
    'stock_quantity': fields.Integer,
    'quantity_unit': fields.String
}

product_complete_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'category_id': fields.Integer,
    'is_active': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'stock_quantity': fields.Integer,
    'stock_unit': fields.String,
    'category': fields.Nested(category_fields),
    'images': fields.List(fields.Nested(product_image_fields)),
    'variants': fields.List(fields.Nested(product_variant_fields))
}


class ProductCompleteListResource(Resource):
    """Get all products with images from B2"""
    
    def get(self):
        """Get all products with full data"""
        try:
            products = Product.query.options(
                joinedload(Product.category),
                joinedload(Product.images),
                joinedload(Product.variants)
            ).all()
            
            result = [marshal(product, product_complete_fields) for product in products]
            
            return {
                'success': True,
                'count': len(result),
                'products': result
            }, 200
        except Exception as e:
            abort(500, message=f"Error fetching products: {str(e)}")


class ProductCompleteResource(Resource):
    """Get single product with images from B2"""
    
    def get(self, product_id):
        """Get product by ID with full data"""
        try:
            product = Product.query.options(
                joinedload(Product.category),
                joinedload(Product.images),
                joinedload(Product.variants)
            ).get(product_id)
            
            if not product:
                abort(404, message=f"Product with id {product_id} not found")
            
            return {
                'success': True,
                'product': marshal(product, product_complete_fields)
            }, 200
        except Exception as e:
            abort(500, message=f"Error fetching product: {str(e)}")


class ProductCreateCompleteResource(Resource):
    """Create product with images and variants"""
    
    def post(self):
        """
        Create product with images and variants in one request
        
        Form-data:
        - name: string (required)
        - description: string
        - category_id: int (required)
        - stock_quantity: int
        - stock_unit: string
        - is_active: int (0 or 1)
        - images: file[] (multiple files, optional)
        - alt_text: string[] (optional)
        
        Variants (can be sent in two ways):
        
        Option 1 - JSON string:
        - variants: JSON string of array
          Example: '[{"variant_name":"Small","variant_price":19.99,"stock_quantity":50,"quantity_unit":"pieces"}]'
        
        Option 2 - Individual fields (can repeat):
        - variant_name[]: string
        - variant_price[]: decimal
        - variant_stock_quantity[]: int
        - variant_quantity_unit[]: string
        """
        try:
            # Get form data
            name = request.form.get('name')
            description = request.form.get('description')
            category_id = request.form.get('category_id')

            # Accept JSON payload fallback for API clients sending JSON
            if (not name or not description or not category_id) and request.is_json:
                json_data = request.get_json(silent=True) or {}
                name = name or json_data.get('name')
                description = description or json_data.get('description')
                category_id = category_id or json_data.get('category_id')
            
            # Validation
            if not name:
                abort(400, message="Product name is required")
            if not category_id:
                abort(400, message="Category ID is required")
            
            try:
                category_id = int(category_id)
            except:
                abort(400, message="Category ID must be an integer")
            
            # Check category exists
            category = Category.query.get(category_id)
            if not category:
                abort(404, message=f"Category with id {category_id} not found")
            
            # Create product
            product = Product(
                name=name,
                description=description,
                category_id=category_id,
                is_active=int(request.form.get('is_active', 1)),
                stock_quantity=int(request.form.get('stock_quantity', 0)),
                stock_unit=request.form.get('stock_unit', 'other')
            )
            
            db.session.add(product)
            db.session.flush()  # Get product ID
            
            # Handle image uploads
            uploaded_images = []
            if 'images' in request.files:
                storage = get_b2_storage()
                files = request.files.getlist('images')
                alt_texts = request.form.getlist('alt_text')
                
                # Validate file types
                ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                
                for idx, file in enumerate(files):
                    if file.filename == '':
                        continue
                    
                    # Check extension
                    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                    if ext not in ALLOWED_EXTENSIONS:
                        continue
                    
                    # Upload to B2
                    upload_result = storage.upload_file(file, folder="products")
                    
                    # Get alt text for this image
                    alt_text = alt_texts[idx] if idx < len(alt_texts) else None
                    
                    # First image is primary
                    is_primary = 1 if idx == 0 else 0
                    
                    # Create database record
                    product_image = ProductImage(
                        product_id=product.id,
                        image_path=upload_result['file_name'],
                        alt_text=alt_text,
                        is_primary=is_primary
                    )
                    
                    db.session.add(product_image)
                    uploaded_images.append({
                        'file_name': upload_result['file_name'],
                        'file_url': upload_result['file_url']
                    })
            
            # Handle variants
            created_variants = []
            
            # Option 1: JSON string format
            if 'variants' in request.form and request.form.get('variants'):
                import json
                try:
                    variants_data = json.loads(request.form.get('variants'))
                    if isinstance(variants_data, list):
                        for var in variants_data:
                            if 'variant_name' in var and 'variant_price' in var:
                                variant = ProductVariant(
                                    product_id=product.id,
                                    variant_name=var['variant_name'],
                                    variant_price=float(var['variant_price']),
                                    stock_quantity=int(var.get('stock_quantity', 0)),
                                    quantity_unit=var.get('quantity_unit')
                                )
                                db.session.add(variant)
                                db.session.flush()
                                created_variants.append({
                                    'id': variant.id,
                                    'variant_name': variant.variant_name,
                                    'variant_price': float(variant.variant_price)
                                })
                except Exception as e:
                    print(f"Error parsing variants JSON: {e}")
            
            # Option 2: Array fields format
            else:
                variant_names = request.form.getlist('variant_name[]') or request.form.getlist('variant_name')
                variant_prices = request.form.getlist('variant_price[]') or request.form.getlist('variant_price')
                variant_stocks = request.form.getlist('variant_stock_quantity[]') or request.form.getlist('variant_stock_quantity')
                variant_units = request.form.getlist('variant_quantity_unit[]') or request.form.getlist('variant_quantity_unit')
                
                # Create variants from array fields
                for idx, name in enumerate(variant_names):
                    if name and idx < len(variant_prices):
                        try:
                            variant = ProductVariant(
                                product_id=product.id,
                                variant_name=name,
                                variant_price=float(variant_prices[idx]),
                                stock_quantity=int(variant_stocks[idx]) if idx < len(variant_stocks) else 0,
                                quantity_unit=variant_units[idx] if idx < len(variant_units) else None
                            )
                            db.session.add(variant)
                            db.session.flush()
                            created_variants.append({
                                'id': variant.id,
                                'variant_name': variant.variant_name,
                                'variant_price': float(variant.variant_price)
                            })
                        except Exception as e:
                            print(f"Error creating variant {idx}: {e}")
            
            db.session.commit()
            
            # Reload product with all relationships
            product = Product.query.options(
                joinedload(Product.category),
                joinedload(Product.images),
                joinedload(Product.variants)
            ).get(product.id)
            
            return {
                'success': True,
                'message': 'Product created successfully',
                'images_uploaded': len(uploaded_images),
                'variants_created': len(created_variants),
                'product': marshal(product, product_complete_fields)
            }, 201
            
        except HTTPException:
            # Re-raise HTTPExceptions like abort(400/404) so they return the correct HTTP status
            raise
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error creating product: {str(e)}")


class ProductUploadImagesResource(Resource):
    """Upload images to existing product"""
    
    def post(self, product_id):
        """
        Upload images to existing product
        
        Form-data:
        - images: file[] (required)
        - alt_text: string[] (optional)
        """
        # Check product exists
        product = Product.query.get(product_id)
        if not product:
            abort(404, message=f"Product with id {product_id} not found")
        
        # Check for files
        if 'images' not in request.files:
            abort(400, message="No images provided")
        
        files = request.files.getlist('images')
        if not files or files[0].filename == '':
            abort(400, message="No images selected")
        
        try:
            storage = get_b2_storage()
            alt_texts = request.form.getlist('alt_text')
            uploaded_images = []
            errors = []
            
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            
            for idx, file in enumerate(files):
                if file.filename == '':
                    continue
                
                # Validate extension
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                if ext not in ALLOWED_EXTENSIONS:
                    errors.append(f"File {file.filename} has invalid extension")
                    continue
                
                try:
                    # Upload to B2
                    upload_result = storage.upload_file(file, folder="products")
                    
                    alt_text = alt_texts[idx] if idx < len(alt_texts) else None
                    
                    # Check if this is the first image for the product
                    existing_images_count = ProductImage.query.filter_by(product_id=product_id).count()
                    is_primary = 1 if existing_images_count == 0 and idx == 0 else 0
                    
                    # Create database record
                    product_image = ProductImage(
                        product_id=product_id,
                        image_path=upload_result['file_name'],
                        alt_text=alt_text,
                        is_primary=is_primary
                    )
                    
                    db.session.add(product_image)
                    db.session.flush()
                    
                    uploaded_images.append({
                        'id': product_image.id,
                        'image_path': upload_result['file_name'],
                        'image_url': upload_result['file_url'],
                        'alt_text': alt_text,
                        'is_primary': is_primary
                    })
                    
                except Exception as e:
                    errors.append(f"Failed to upload {file.filename}: {str(e)}")
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f"{len(uploaded_images)} image(s) uploaded successfully",
                'images': uploaded_images,
                'errors': errors
            }, 201
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error uploading images: {str(e)}")


class ProductImageDeleteResource(Resource):
    """Delete product image"""
    
    def delete(self, image_id):
        """Delete image from database and B2"""
        image = ProductImage.query.get(image_id)
        
        if not image:
            abort(404, message=f"Image with id {image_id} not found")
        
        try:
            # Delete from B2
            storage = get_b2_storage()
            storage.delete_file(image.image_path)
            
            # Delete from database
            db.session.delete(image)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Image deleted successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error deleting image: {str(e)}")


class ProductAddVariantsResource(Resource):
    """Add or update variants for a product"""
    
    def post(self, product_id):
        """
        Add variants to existing product
        
        JSON body:
        {
            "variants": [
                {
                    "variant_name": "Small - 500ml",
                    "variant_price": 19.99,
                    "stock_quantity": 100,
                    "quantity_unit": "bottles"
                },
                {
                    "variant_name": "Large - 1L",
                    "variant_price": 34.99,
                    "stock_quantity": 50,
                    "quantity_unit": "bottles"
                }
            ]
        }
        """
        product = Product.query.get(product_id)
        if not product:
            abort(404, message=f"Product with id {product_id} not found")
        
        data = request.get_json()
        if not data or 'variants' not in data:
            abort(400, message="Variants data is required")
        
        variants_data = data['variants']
        if not isinstance(variants_data, list):
            abort(400, message="Variants must be an array")
        
        try:
            created_variants = []
            
            for var in variants_data:
                if 'variant_name' not in var or 'variant_price' not in var:
                    continue
                
                variant = ProductVariant(
                    product_id=product_id,
                    variant_name=var['variant_name'],
                    variant_price=float(var['variant_price']),
                    stock_quantity=int(var.get('stock_quantity', 0)),
                    quantity_unit=var.get('quantity_unit')
                )
                
                db.session.add(variant)
                db.session.flush()
                
                created_variants.append({
                    'id': variant.id,
                    'variant_name': variant.variant_name,
                    'variant_price': float(variant.variant_price),
                    'stock_quantity': variant.stock_quantity,
                    'quantity_unit': variant.quantity_unit
                })
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'{len(created_variants)} variant(s) added successfully',
                'variants': created_variants
            }, 201
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error adding variants: {str(e)}")


class ProductUpdateResource(Resource):
    """Update product details"""
    
    def patch(self, product_id):
        """
        Update product
        
        JSON body:
        {
            "name": "New name",
            "description": "New description",
            "category_id": 2,
            "is_active": 1,
            "stock_quantity": 100,
            "stock_unit": "Kg"
        }
        """
        product = Product.query.get(product_id)
        if not product:
            abort(404, message=f"Product with id {product_id} not found")
        
        data = request.get_json()
        if not data:
            abort(400, message="No data provided")
        
        try:
            # Update fields
            if 'name' in data:
                product.name = data['name']
            if 'description' in data:
                product.description = data['description']
            if 'category_id' in data:
                category = Category.query.get(data['category_id'])
                if not category:
                    abort(404, message="Category not found")
                product.category_id = data['category_id']
            if 'is_active' in data:
                product.is_active = int(data['is_active'])
            if 'stock_quantity' in data:
                product.stock_quantity = int(data['stock_quantity'])
            if 'stock_unit' in data:
                product.stock_unit = data['stock_unit']
            
            product.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Reload with relationships
            product = Product.query.options(
                joinedload(Product.category),
                joinedload(Product.images),
                joinedload(Product.variants)
            ).get(product_id)
            
            return {
                'success': True,
                'message': 'Product updated successfully',
                'product': marshal(product, product_complete_fields)
            }, 200
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error updating product: {str(e)}")
    
    def delete(self, product_id):
        """Delete product and all related data"""
        product = Product.query.get(product_id)
        if not product:
            abort(404, message=f"Product with id {product_id} not found")
        
        try:
            storage = get_b2_storage()
            
            # Delete all images from B2
            images = ProductImage.query.filter_by(product_id=product_id).all()
            for image in images:
                try:
                    storage.delete_file(image.image_path)
                except:
                    pass  # Continue even if B2 delete fails
            
            # Delete from database (cascade will handle related records)
            db.session.delete(product)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Product and all related data deleted successfully'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error deleting product: {str(e)}")