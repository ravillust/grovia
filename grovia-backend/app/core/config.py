"""
Core configuration settings for the application
"""
from pathlib import Path
from typing import List, Tuple
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
ML_MODELS_DIR = BASE_DIR / "ml_models"
LOG_DIR = BASE_DIR / "logs"

UPLOAD_DIR.mkdir(exist_ok=True)
ML_MODELS_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    BASE_DIR: Path = BASE_DIR
    UPLOAD_DIR: Path = UPLOAD_DIR
    ML_MODELS_DIR: Path = ML_MODELS_DIR
    LOG_DIR: Path = LOG_DIR

    APP_NAME: str = "Grovia API"
    PROJECT_NAME: str = "Grovia Backend"
    PROJECT_DESCRIPTION: str = "Backend API for Grovia Plant Disease Detection"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ENCRYPTION_KEY: str

    MYSQL_SERVER: str = "localhost"
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str = "grovia_db"
    MYSQL_PORT: int = 3306
    DATABASE_URL: str

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "https://grovia.vercel.app",
    ]

    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp"]
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024

    MODEL_PATH: str = str(ML_MODELS_DIR / "cnn_model.h5")
    LABELS_PATH: str = str(ML_MODELS_DIR / "labels.json")
    IMAGE_SIZE: Tuple[int, int] = (224, 224)

    GEMINI_API_KEY: str

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:5173/auth/google/callback"

    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    USE_CLOUDINARY: bool = False

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = LOG_DIR / "app.log"

    model_config = {
        'env_file': '.env',
        'case_sensitive': True,
        'extra': 'allow'
    }


settings = Settings()
