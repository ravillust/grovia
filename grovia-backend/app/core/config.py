"""
Core configuration settings for the application
"""
import os
from pathlib import Path
from typing import List, Tuple
from pydantic_settings import BaseSettings

# Project Directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
ML_MODELS_DIR = BASE_DIR / "ml_models"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
ML_MODELS_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    """Application settings"""

    # Project Directories
    BASE_DIR: Path = BASE_DIR
    UPLOAD_DIR: Path = UPLOAD_DIR
    ML_MODELS_DIR: Path = ML_MODELS_DIR
    LOG_DIR: Path = LOG_DIR

    # Application
    APP_NAME: str = "Grovia API"
    PROJECT_NAME: str = "Grovia Backend"
    PROJECT_DESCRIPTION: str = "Backend API for Grovia Plant Disease Detection"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "your-super-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ENCRYPTION_KEY: str = "your-32-character-encryption-key"

    # Database - MySQL
    MYSQL_SERVER: str = "localhost"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DB: str = "grovia_db"
    MYSQL_PORT: int = 3306
    DATABASE_URL: str = "mysql+mysqlclient://root:password@localhost:3306/grovia_db"

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://grovia.vercel.app",
    ]

    # Upload Configuration
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB

    # ML Model Configuration
    MODEL_PATH: str = str(ML_MODELS_DIR / "cnn_model.h5")
    LABELS_PATH: str = str(ML_MODELS_DIR / "labels.json")
    IMAGE_SIZE: Tuple[int, int] = (224, 224)

    # Gemini AI
    GEMINI_API_KEY: str = ""

    # Cloudinary Configuration (for production image storage)
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    USE_CLOUDINARY: bool = False  # Set True in production

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = LOG_DIR / "app.log"

    model_config = {
        'env_file': '.env',
        'case_sensitive': True,
        'extra': 'allow'
    }


settings = Settings()
