import os
import hashlib
import mimetypes
from datetime import datetime
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from werkzeug.utils import secure_filename

class B2Storage:
    """Backblaze B2 Storage Handler"""
    
    def __init__(self):
        # Get credentials from environment
        self.application_key_id = os.getenv('B2_KEY_ID')
        self.application_key = os.getenv('B2_APP_KEY')
        self.bucket_name = os.getenv('B2_BUCKET_NAME')
        
        if not all([self.application_key_id, self.application_key, self.bucket_name]):
            raise ValueError("B2 credentials not found in environment variables")
        
        # Initialize B2 API
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api.authorize_account("production", self.application_key_id, self.application_key)
        
        # Get bucket
        self.bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
    
    def get_file_url(self, file_path):
        """Get public URL for a file"""
        if not file_path:
            return None
        # Use the download URL format
        return f"https://f002.backblazeb2.com/file/{self.bucket_name}/{file_path}"
    
    def generate_unique_filename(self, original_filename):
        """Generate unique filename"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        random_hash = hashlib.md5(f"{original_filename}{timestamp}".encode()).hexdigest()[:8]
        name, ext = os.path.splitext(secure_filename(original_filename))
        return f"{timestamp}_{random_hash}_{name}{ext}"
    
    def upload_file(self, file, folder="products"):
        """Upload file to B2 storage"""
        try:
            unique_filename = self.generate_unique_filename(file.filename)
            file_path = f"{folder}/{unique_filename}"
            content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
            
            # Read file data
            file_data = file.read()
            file.seek(0)  # Reset file pointer
            
            # Upload to B2
            file_info = self.bucket.upload_bytes(
                data_bytes=file_data,
                file_name=file_path,
                content_type=content_type
            )
            
            return {
                'file_name': file_path,
                'file_url': self.get_file_url(file_path),
                'file_id': file_info.id_,
                'content_type': content_type,
                'size': len(file_data)
            }
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def delete_file(self, file_name):
        """Delete file from B2"""
        try:
            file_version = self.bucket.get_file_info_by_name(file_name)
            self.b2_api.delete_file_version(file_version.id_, file_name)
            return True
        except Exception as e:
            print(f"Warning: Could not delete file {file_name}: {str(e)}")
            return False

# Initialize global instance
b2_storage = None

def get_b2_storage():
    """Get or create B2Storage instance"""
    global b2_storage
    if b2_storage is None:
        b2_storage = B2Storage()
    return b2_storage