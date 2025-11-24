"""
Detection endpoint untuk deteksi penyakit tanaman
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Request
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.utils.timezone_utils import resolve_user_timezone
from typing import Optional
import logging

from app.database import get_db
from app.dependencies import get_current_active_user, validate_image_file
from app.models.user import User
from app.schemas.detection import DetectionResult, TreatmentRecommendation
from app.crud import detection as detection_crud
from app.crud import disease as disease_crud
from app.core.config import settings
from app.core.exceptions import DetectionError, NotFoundError
from app.utils.cloudinary_service import get_cloudinary_service

# Import Gemini AI Model for better accuracy
from app.ml.gemini_model import get_gemini_model as get_model
from app.ml.leaf_validator import get_leaf_validator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/detect", response_model=dict)
async def detect_disease(
    image: UploadFile = File(...),
    request: Request = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload image and detect plant disease
    UC04, UC05: Deteksi penyakit tanaman
    NF06: Maximum 25 seconds processing time
    """

    logger.info(f"Detection request from user {current_user.id}")

    # Validate image file
    validate_image_file(image)

    # Create upload directory if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(image.filename)[1]
    filename = f"user_{current_user.id}_{timestamp}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    try:
        # Save uploaded file
        logger.info(f"Saving file to {file_path}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # STEP 1: Validate if image is a leaf/plant BEFORE detection
        # Using OpenCV (FREE - no API usage!)
        logger.info("Validating if image is a leaf (OpenCV)...")
        leaf_validator = get_leaf_validator()

        validation_result = leaf_validator.validate(file_path)

        if not validation_result.get("is_valid", False):
            # Image is NOT a leaf - reject immediately (NO API USED!)
            logger.warning(f"Invalid image rejected: {validation_result.get('detected_content')}")

            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

            # Return simple user-friendly error message
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pastikan Anda mengupload foto daun tanaman"
            )

        logger.info(f"✅ Image validated as leaf (confidence: {validation_result.get('confidence')}%)")

        # STEP 2: Perform disease detection FIRST (before cloud upload)
        # Get ML model instance
        ml_model = get_model()

        # Perform detection (ML model inference)
        logger.info("Running disease detection...")
        prediction = ml_model.predict(file_path)

        if not prediction:
            logger.error("ML model returned None/empty prediction")
            # Clean up local file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise DetectionError("Failed to detect disease - model returned no prediction")

        logger.info(f"✅ Prediction received: {prediction.get('disease_name', 'Unknown')}")

        # STEP 3: Upload to cloud storage (if enabled) AFTER detection success
        image_url = f"/uploads/{filename}"  # Default: local storage
        cloudinary_public_id = None

        if settings.USE_CLOUDINARY:
            try:
                logger.info("Uploading image to Cloudinary...")
                cloudinary = get_cloudinary_service()
                upload_result = cloudinary.upload_image(
                    file_path=file_path,
                    folder="grovia/detections",
                    public_id=f"user_{current_user.id}_{timestamp}"
                )
                image_url = upload_result["url"]
                cloudinary_public_id = upload_result["public_id"]
                logger.info(f"✅ Image uploaded to Cloudinary: {image_url}")

                # Delete local file after successful upload
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info("Local file deleted after cloud upload")
            except Exception as e:
                logger.warning(f"Cloudinary upload failed, using local storage: {e}")
                # Fallback to local storage if cloud upload fails

        # STEP 4: Format prediction results

        # Ensure confidence is properly formatted (0-1 range)
        if "confidence" in prediction:
            prediction["confidence"] = round(float(prediction["confidence"]), 4)

        # Add confidence_percent with max 2 decimal places (clean display)
        if "confidence_percent" not in prediction and "confidence" in prediction:
            prediction["confidence_percent"] = round(prediction["confidence"] * 100, 2)
        else:
            # If confidence_percent already exists, ensure it's rounded to 2 decimals
            prediction["confidence_percent"] = round(float(prediction["confidence_percent"]), 2)

        logger.info(f"Prediction: {prediction['disease_name']} ({prediction['confidence_percent']}%)")

        # Database operations can be done asynchronously/optionally
        # Don't let DB slow down the response
        disease = None
        history = None

        # Quick response preparation (do this first before slow DB operations)
        # Determine detected_at in user's timezone for display (header -> profile -> default)
        local_tz = resolve_user_timezone(request, current_user)

        response_data = {
            "success": True,
            "data": {
                "detection_id": None,  # Will be updated if history saved
                "disease_id": prediction["disease_id"],
                "disease_name": prediction["disease_name"],
                "scientific_name": prediction.get("scientific_name", ""),
                "confidence": prediction["confidence"],
                "confidence_percent": prediction["confidence_percent"],
                "is_healthy": prediction.get("is_healthy", False),
                "image_url": image_url,
                "description": prediction.get("analysis_notes", ""),
                "symptoms": prediction.get("symptoms", []),
                "recommendations": prediction.get("recommendations", []),
                "all_predictions": prediction.get("all_predictions", []),
                "detected_at": datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(local_tz).isoformat()
            }
        }

        # Optional: Try to get disease details from database (don't block response)
        try:
            disease = disease_crud.get_disease_by_id(db, prediction["disease_id"])
            if disease:
                response_data["data"]["description"] = disease.description or response_data["data"]["description"]
                logger.info(f"Enhanced with DB data: {disease.disease_name}")
        except Exception as e:
            logger.warning(f"Could not fetch disease from DB: {e} (using Gemini data)")

        # Optional: Create detection history (don't block response)
        try:
            # Store the appropriate path based on storage type
            stored_image_path = image_url if settings.USE_CLOUDINARY else f"uploads/{filename}"

            history = detection_crud.create_detection_history(
                db=db,
                user_id=current_user.id,
                disease_id=prediction["disease_id"],
                disease_name=prediction["disease_name"],
                scientific_name=prediction.get("scientific_name", ""),
                confidence=prediction["confidence"],
                image_url=stored_image_path,
                description=disease.description if disease else prediction.get("analysis_notes", ""),
                symptoms=None
            )
            
            # Commit to database
            db.commit()
            db.refresh(history)
            
            # Convert stored history detected_at (UTC) to user's timezone for response
            response_data["data"]["detection_id"] = history.id
            if hasattr(history, "detected_at") and history.detected_at is not None:
                try:
                    # Convert UTC to local timezone
                    utc_time = history.detected_at.replace(tzinfo=timezone.utc)
                    local_time = utc_time.astimezone(local_tz)
                    response_data["data"]["detected_at"] = local_time.isoformat()
                except Exception as e:
                    logger.warning(f"Timezone conversion error: {e}")
                    # fallback to UTC string
                    response_data["data"]["detected_at"] = history.detected_at.replace(tzinfo=timezone.utc).isoformat()
            logger.info(f"✅ History saved: ID {history.id}")
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
            db.rollback()
            # Don't fail the whole request if history saving fails

        logger.info("Detection completed successfully")
        return response_data

    except HTTPException as http_exc:
        # Re-raise HTTPException as-is (proper HTTP errors)
        logger.warning(f"HTTP Exception: {http_exc.detail}")
        # Clean up uploaded file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise http_exc

    except DetectionError as e:
        logger.error(f"Detection error: {str(e)}")
        # Clean up uploaded file on error
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        # Clean up uploaded file on error
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}"
        )


@router.get("/treatment/{disease_id}", response_model=dict)
async def get_treatment_recommendation(
    disease_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get treatment recommendation for specific disease
    UC06: Rekomendasi perawatan

    NOTE: Recommendations are already included in detection response.
    This endpoint is for additional treatment details from database (optional).
    """

    logger.info(f"Fetching treatment for disease: {disease_id}")

    try:
        # Get treatment from database
        treatment = disease_crud.get_treatment_recommendation(db, disease_id)

        if not treatment:
            # Return empty recommendations instead of error
            # Since detection response already has recommendations from Gemini
            logger.warning(f"Treatment for disease '{disease_id}' not found in DB")
            return {
                "success": True,
                "data": {
                    "disease_id": disease_id,
                    "disease_name": "Unknown",
                    "prevention": [],
                    "treatment": [],
                    "organic_solutions": [],
                    "chemical_solutions": [],
                    "additional_tips": []
                }
            }

        return {
            "success": True,
            "data": treatment
        }
    except Exception as e:
        logger.error(f"Error fetching treatment: {str(e)}")
        # Return empty instead of error to not break frontend
        return {
            "success": True,
            "data": {
                "disease_id": disease_id,
                "disease_name": "Unknown",
                "prevention": [],
                "treatment": [],
                "organic_solutions": [],
                "chemical_solutions": [],
                "additional_tips": []
            }
        }


@router.post("/history", response_model=dict, status_code=status.HTTP_201_CREATED)
async def save_detection_history(
    detection_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Save detection result to history
    """

    try:
        history = detection_crud.create_detection_history(
            db=db,
            user_id=current_user.id,
            disease_id=detection_data["disease_id"],
            disease_name=detection_data["disease_name"],
            scientific_name=detection_data.get("scientific_name", ""),
            confidence=detection_data["confidence"],
            image_url=detection_data["image_url"],
            description=detection_data.get("description"),
            symptoms=detection_data.get("symptoms")
        )

        return {
            "success": True,
            "data": {
                "history_id": history.id,
                "message": "Detection history saved successfully"
            }
        }

    except Exception as e:
        logger.error(f"Failed to save history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save history: {str(e)}"
        )


@router.get("/model-info")
async def get_model_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get ML model information
    """
    try:
        ml_model = get_model()
        model_info = ml_model.get_info()

        return {
            "success": True,
            "data": model_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )


@router.get("/supported-diseases")
async def get_supported_diseases():
    """
    Get list of diseases that can be detected
    Tidak perlu login untuk endpoint ini
    """
    try:
        ml_model = get_model()
        model_info = ml_model.get_info()

        diseases = model_info.get("diseases", [])

        return {
            "success": True,
            "data": {
                "diseases": diseases,
                "total": len(diseases)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get supported diseases: {str(e)}"
        )