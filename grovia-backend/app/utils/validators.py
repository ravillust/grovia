"""
Validation utilities for the application
"""

import re
from typing import Optional
from fastapi import HTTPException
from PIL import Image
import io


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    
    return True, None


def validate_image(image_bytes: bytes, max_size: int = 10 * 1024 * 1024) -> tuple[bool, Optional[str]]:
    """
    Validate uploaded image
    
    Args:
        image_bytes: Image bytes to validate
        max_size: Maximum allowed file size in bytes (default: 10MB)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    if len(image_bytes) > max_size:
        return False, "Image size exceeds maximum allowed size (10MB)"
    
    try:
        # Try to open image to verify format
        image = Image.open(io.BytesIO(image_bytes))
        
        # Check if format is supported
        if image.format not in ['JPEG', 'JPG', 'PNG']:
            return False, "Unsupported image format. Please use JPEG or PNG"
        
        # Check minimum dimensions
        if image.size[0] < 224 or image.size[1] < 224:
            return False, "Image dimensions too small. Minimum size is 224x224 pixels"
            
        return True, None
        
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def validate_pagination_params(page: int, limit: int) -> None:
    """
    Validate pagination parameters
    
    Args:
        page: Page number
        limit: Items per page
        
    Raises:
        HTTPException if parameters are invalid
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be greater than 0")
    
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100 items per page")
