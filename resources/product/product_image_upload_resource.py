from flask import request
from flask_restful import Resource, abort
from models.product import Product
from models.product_image import ProductImage
from extensions import db
from utils.b2_storage import B2Storage
from werkzeug.datastructures import FileStorage

# Initialize B2 Storage
b2_storage = B2Storage()

class ProductImageUploadResource(Resource):
    """
    Upload images for a product
    """
    def post(self, product_id):
        """
        Upload one or multiple images for a product
        
        Form-data:
            - images: file (can be multiple)
            - alt_text: string (optional, can be array for multiple)
            - is_primary: int (0 or 1, optional)
        """
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            abort(404, message=f"Product with id {product_id} not found")
        
        # Check if files are in request
        if 'images' not in request.files:
            abort(400, message="No images provided")
        
        files = request.files.getlist('images')
        
        if not files or files[0].filename == '':
            abort(400, message="No images selected")
        
        # Validate file types
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        # Filter valid files
        valid_files = [f for f in files if allowed_file(f.filename)]
        
        if not valid_files:
            abort(400, message="No valid image files provided. Allowed: png, jpg, jpeg, gif, webp")
        
        try:
            # Upload files to B2
            upload_results = b2_storage.upload_multiple_files(valid_files, folder="products")
            
            # Get alt_text and is_primary from form
            alt_texts = request.form.getlist('alt_text')
            is_primary_flags = request.form.getlist('is_primary')
            
            # Create database entries
            created_images = []
            
            for idx, result in enumerate(upload_results['success']):
                # Get alt_text for this image
                alt_text = alt_texts[idx] if idx < len(alt_texts) else None
                
                # Get is_primary for this image
                is_primary = 0
                if idx < len(is_primary_flags):
                    try:
                        is_primary = int(is_primary_flags[idx])
                    except:
                        is_primary = 0
                
                # If this is the first image and no primary is set, make it primary
                if idx == 0 and not any(is_primary_flags):
                    is_primary = 1
                
                # Create ProductImage record
                product_image = ProductImage(
                    product_id=product_id,
                    image_path=result['file_name'],  # Store the B2 path
                    alt_text=alt_text,
                    is_primary=is_primary
                )
                
                db.session.add(product_image)
                db.session.flush()
                
                created_images.append({
                    'id': product_image.id,
                    'image_path': result['file_name'],
                    'image_url': result['file_url'],  # Full public URL
                    'alt_text': alt_text,
                    'is_primary': is_primary,
                    'size': result['size'],
                    'content_type': result['content_type']
                })
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f"{len(created_images)} image(s) uploaded successfully",
                'images': created_images,
                'upload_stats': {
                    'total': upload_results['total'],
                    'uploaded': upload_results['uploaded'],
                    'failed': upload_results['failed']
                },
                'errors': upload_results['errors']
            }, 201
            
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error uploading images: {str(e)}")


class ProductImageDeleteResource(Resource):
    """
    Delete a product image (from database and B2 storage)
    """
    def delete(self, image_id):
        """
        Delete a product image
        """
        image = ProductImage.query.get(image_id)
        
        if not image:
            abort(404, message=f"Image with id {image_id} not found")
        
        try:
            # Delete from B2 storage
            b2_storage.delete_file(image.image_path)
            
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
