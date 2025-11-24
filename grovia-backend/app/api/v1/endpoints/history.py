from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from datetime import timezone, timedelta
import json
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.crud import detection as detection_crud
from app.core.exceptions import NotFoundError
from app.utils.timezone_utils import resolve_user_timezone

router = APIRouter()


def convert_to_local_time(dt, local_tz):
    """Convert UTC datetime to local timezone"""
    if dt is None:
        return None
    
    # Ensure datetime is timezone-aware (UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Convert to local timezone
    return dt.astimezone(local_tz)


@router.get("", response_model=dict)
async def get_history(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    sort: str = Query("newest", regex="^(newest|oldest)$", description="Sort order"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's detection history with pagination
    UC07: Riwayat deteksi
    """

    # Get user's timezone
    local_tz = resolve_user_timezone(request, current_user)

    # Get paginated history
    items, total = detection_crud.get_detection_history(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit,
        sort=sort
    )

    # Calculate pagination info
    total_pages = (total + limit - 1) // limit

    # Format response
    history_items = []
    for item in items:
        # Convert UTC to local timezone
        local_detected_at = convert_to_local_time(item.detected_at, local_tz)
        
        # Generate full image URL (accessible from frontend)
        # Support both local storage and Cloudinary URLs
        if item.image_url.startswith("http://") or item.image_url.startswith("https://"):
            # Already a full URL (Cloudinary)
            full_image_url = item.image_url
        else:
            # Local storage - generate full URL
            image_filename = item.image_url.replace("uploads\\", "").replace("uploads/", "")
            full_image_url = f"http://localhost:8000/uploads/{image_filename}"

        history_items.append({
            "id": item.id,  # Add 'id' for easier frontend access
            "history_id": item.id,
            "disease_id": item.disease_id,
            "disease_name": item.disease_name,
            "scientific_name": item.scientific_name or "",
            "confidence": round(item.confidence, 4),
            "confidence_percent": round(item.confidence * 100, 2),  # Add percentage format
            "image_url": full_image_url,  # Full URL with base URL
            "image_path": item.image_url,  # Original path (for reference)
            "detected_at": local_detected_at.isoformat(),  # Local timezone
            "date": local_detected_at.strftime("%Y-%m-%d"),  # Formatted date in local time
            "time": local_detected_at.strftime("%H:%M:%S")   # Formatted time in local time
        })

    return {
        "success": True,
        "data": {
            "items": history_items,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total,
                "items_per_page": limit,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        },
        "message": f"Found {total} detection records"
    }


@router.get("/{history_id}", response_model=dict)
async def get_history_detail(
    history_id: int,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get specific detection history detail
    """

    # Get user's timezone
    local_tz = resolve_user_timezone(request, current_user)

    # Get history item
    history = detection_crud.get_detection_by_id(
        db=db,
        history_id=history_id,
        user_id=current_user.id
    )

    if not history:
        raise NotFoundError("History not found")

    # Convert UTC to local timezone
    local_detected_at = convert_to_local_time(history.detected_at, local_tz)

    # Parse symptoms if exists
    symptoms = []
    if history.symptoms:
        try:
            symptoms = json.loads(history.symptoms)
        except:
            symptoms = []

    # Generate full image URL (support both local and Cloudinary)
    if history.image_url.startswith("http://") or history.image_url.startswith("https://"):
        # Already a full URL (Cloudinary)
        full_image_url = history.image_url
    else:
        # Local storage - generate full URL
        image_filename = history.image_url.replace("uploads\\", "").replace("uploads/", "")
        full_image_url = f"http://localhost:8000/uploads/{image_filename}"

    return {
        "success": True,
        "data": {
            "history_id": history.id,
            "disease_id": history.disease_id,
            "disease_name": history.disease_name,
            "scientific_name": history.scientific_name,
            "confidence": round(history.confidence, 4),
            "confidence_percent": round(history.confidence * 100, 2),
            "image_url": full_image_url,
            "image_path": history.image_url,
            "description": history.description,
            "symptoms": symptoms,
            "detected_at": local_detected_at.isoformat()  # Local timezone
        }
    }


@router.delete("/{history_id}", response_model=dict)
async def delete_history(
    history_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete detection history
    """

    # Delete history
    success = detection_crud.delete_detection_history(
        db=db,
        history_id=history_id,
        user_id=current_user.id
    )

    if not success:
        raise NotFoundError("History not found")

    return {
        "success": True,
        "message": "History deleted successfully"
    }


@router.get("/stats/summary", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user detection statistics
    """

    total_detections = detection_crud.get_user_detection_count(
        db=db,
        user_id=current_user.id
    )

    return {
        "success": True,
        "data": {
            "total_detections": total_detections,
            "user_id": current_user.id
        }
    }