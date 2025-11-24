"""
Cloudinary Storage Service
Handles image uploads to Cloudinary cloud storage for production
"""
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from typing import Dict, Optional
import logging
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


class CloudinaryService:
    """Service for handling Cloudinary image uploads"""

    def __init__(self):
        """Initialize Cloudinary configuration"""
        if settings.USE_CLOUDINARY:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True
            )
            logger.info("Cloudinary configured for production use")
        else:
            logger.info("Using local storage (development mode)")

    def upload_image(
        self,
        file_path: str,
        folder: str = "grovia/detections",
        public_id: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Upload image to Cloudinary

        Args:
            file_path: Path to local image file
            folder: Cloudinary folder name
            public_id: Optional custom public ID

        Returns:
            Dict with upload result (url, public_id, etc.)
        """
        if not settings.USE_CLOUDINARY:
            raise ValueError("Cloudinary is not enabled. Set USE_CLOUDINARY=true in .env")

        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_path,
                folder=folder,
                public_id=public_id,
                resource_type="image",
                overwrite=True,
                quality="auto",  # Auto optimize quality
                fetch_format="auto"  # Auto format (WebP when supported)
            )

            logger.info(f"Image uploaded to Cloudinary: {upload_result['public_id']}")

            return {
                "url": upload_result["secure_url"],
                "public_id": upload_result["public_id"],
                "format": upload_result["format"],
                "width": upload_result["width"],
                "height": upload_result["height"],
                "bytes": upload_result["bytes"]
            }

        except Exception as e:
            logger.error(f"Cloudinary upload error: {e}")
            raise Exception(f"Failed to upload image to Cloudinary: {str(e)}")

    def delete_image(self, public_id: str) -> bool:
        """
        Delete image from Cloudinary

        Args:
            public_id: Cloudinary public ID

        Returns:
            True if successful
        """
        if not settings.USE_CLOUDINARY:
            raise ValueError("Cloudinary is not enabled")

        try:
            result = cloudinary.uploader.destroy(public_id)
            logger.info(f"Image deleted from Cloudinary: {public_id}")
            return result.get("result") == "ok"
        except Exception as e:
            logger.error(f"Cloudinary delete error: {e}")
            return False

    def get_optimized_url(
        self,
        public_id: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: str = "auto"
    ) -> str:
        """
        Get optimized image URL with transformations

        Args:
            public_id: Cloudinary public ID
            width: Target width
            height: Target height
            quality: Quality setting (auto, best, good, eco, low)

        Returns:
            Optimized image URL
        """
        transformations = {
            "quality": quality,
            "fetch_format": "auto"
        }

        if width:
            transformations["width"] = width
        if height:
            transformations["height"] = height

        url, _ = cloudinary_url(public_id, **transformations)
        return url


# Global instance
_cloudinary_service = None


def get_cloudinary_service() -> CloudinaryService:
    """Get or create Cloudinary service instance"""
    global _cloudinary_service
    if _cloudinary_service is None:
        _cloudinary_service = CloudinaryService()
    return _cloudinary_service
