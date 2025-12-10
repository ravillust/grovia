"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import api_router
# Switch to Gemini AI Model for better accuracy
from app.ml.gemini_model import load_gemini_model as load_ml_model

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(settings.LOG_FILE)),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for the FastAPI application
    """
    # Startup
    logger.info("Starting Grovia Backend API...")
    logger.info("Loading ML model...")
    load_ml_model()
    logger.info("Application startup complete")
    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# Add CORS middleware - Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://grovia-five.vercel.app/"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "message": "Grovia API is running"
    }

# Root redirect to docs
@app.get("/")
async def root():
    """
    Redirect root to API documentation
    """
    return {"message": "Welcome to Grovia API", "docs_url": "/docs"}
