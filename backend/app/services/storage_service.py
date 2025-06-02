# Storage Cloudnary Service
import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import settings
import logging
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class CloudinaryStorage:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )

    def upload_image_from_bytes(self, image_data: bytes, filename: str, folder: str = "youtube-thumbnails") -> dict:
        """Upload image from bytes data to Cloudinary"""
        try:
            # Encode bytes to base64
            encoded_data = base64.b64encode(image_data).decode('utf-8')
            data_url = f"data:image/png;base64,{encoded_data}"
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                data_url,
                public_id=filename.split('.')[0],
                folder=folder,
                resource_type="image",
                format="png",
                quality="95",
                fetch_format="auto",
                transformation=[
                    {"width": 1280, "height": 720, "crop": "fill", "quality": "95"}
                ]
            )
            
            print(f"Cloudinary upload successful: {result['secure_url']}")
            
            return {
                "success": True,
                "url": result['secure_url'],
                "download_url": self._generate_download_url(result['public_id']),
                "thumbnail_url": self._generate_thumbnail_url(result['public_id']),
                "preview_url": self._generate_preview_url(result['public_id']),
                "public_id": result['public_id'],
                "bytes": result.get('bytes', 0),
                "format": result.get('format', 'jpg')
            }
            
        except Exception as e:
            logger.error(f"Cloudinary upload from bytes failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
    
    def upload_image(self, image_path: str, filename: str, folder: str = "youtube-thumbnails") -> dict:
        """Upload image to Cloudinary with multiple size variants"""
        try:
            # Upload original image
            result = cloudinary.uploader.upload(
                image_path,
                public_id=filename.split('.')[0],
                folder=folder,
                resource_type="image",
                format="png",
                quality="95",
                fetch_format="auto",
                transformation=[
                    {"width": 1280, "height": 720, "crop": "fill", "quality": "95"}
                ]
            )
            
            # Generate different URLs for different purposes
            base_url = result['secure_url']
            
            return {
                "success": True,
                "url": base_url,  # Original high quality
                "download_url": self._generate_download_url(result['public_id']),
                "thumbnail_url": self._generate_thumbnail_url(result['public_id']),
                "preview_url": self._generate_preview_url(result['public_id']),
                "public_id": result['public_id'],
                "bytes": result.get('bytes', 0),
                "format": result.get('format', 'jpg')
            }
            
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _generate_download_url(self, public_id: str) -> str:
        """Generate URL with download attachment"""
        return cloudinary.utils.cloudinary_url(
            public_id,
            format="png",
            quality="95",
            flags="attachment:youtube-thumbnail"
        )[0]
    
    def _generate_thumbnail_url(self, public_id: str) -> str:
        """Generate small thumbnail for previews"""
        return cloudinary.utils.cloudinary_url(
            public_id,
            width=400,
            height=300,
            crop="fill",
            quality="95"
        )[0]
        
    def _generate_preview_url(self, public_id: str) -> str:
        """Generate medium size for web display"""
        return cloudinary.utils.cloudinary_url(
            public_id,
            width=800,
            height=450,
            crop="fill",
            quality="95"
        )[0]
        
    def delete_image(self, public_id: str) -> bool:
        """Delete image from Cloudinary"""
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Failed to delete image {public_id}: {e}")
            return False
        
    def get_usage_stats(self) -> dict:
        """Get current usage statistics"""
        try:
            result = cloudinary.api.usage()
            return {
                "storage_used": result.get('storage', {}).get('usage', 0),
                "storage_limit": result.get('storage', {}).get('limit', 0),
                "bandwidth_used": result.get('bandwidth', {}).get('usage', 0),
                "bandwidth_limit": result.get('bandwidth', {}).get('limit', 0),
                "requests_used": result.get('requests', {}).get('usage', 0),
                "requests_limit": result.get('requests', {}).get('limit', 0)
            }
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {}