"""
Models package initialization
File: app/models/__init__.py
Import semua model agar ter-register di Base.metadata
"""

from app.database import Base

# Import semua model secara eksplisit
from app.models.user import User
from app.models.detection_history import DetectionHistory


# Export untuk kemudahan import
__all__ = [
    "Base",
    "User",
    "DetectionHistory"
]