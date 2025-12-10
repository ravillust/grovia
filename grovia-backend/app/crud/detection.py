from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from typing import List, Optional, Tuple
import json
from app.models.detection_history import DetectionHistory
from app.schemas.detection import DetectionHistoryCreate


def create_detection_history(
    db: Session,
    user_id: int,
    disease_id: str,
    disease_name: str,
    scientific_name: Optional[str],
    confidence: float,
    image_url: str,
    description: Optional[str] = None,
    symptoms: Optional[List[str]] = None
) -> DetectionHistory:
    """Create detection history record"""
    
    symptoms_json = json.dumps(symptoms) if symptoms else None
    
    db_history = DetectionHistory(
        user_id=user_id,
        disease_id=disease_id,
        disease_name=disease_name,
        scientific_name=scientific_name or "",
        confidence=confidence,
        image_url=image_url,
        description=description or "",
        symptoms=symptoms_json
    )
    
    db.add(db_history)
    # Don't commit here - let the caller handle commit
    # db.commit()
    # db.refresh(db_history)
    
    return db_history


def get_detection_history(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 10,
    sort: str = "newest"
) -> Tuple[List[DetectionHistory], int]:
    """Get paginated detection history"""
    query = db.query(DetectionHistory).filter(DetectionHistory.user_id == user_id)
    
    # Count total items
    total = query.count()
    
    # Apply sorting
    if sort == "oldest":
        query = query.order_by(asc(DetectionHistory.detected_at))
    else:  # newest (default)
        query = query.order_by(desc(DetectionHistory.detected_at))
    
    # Apply pagination
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()
    
    return items, total


def get_detection_by_id(db: Session, history_id: int, user_id: int) -> Optional[DetectionHistory]:
    """Get specific detection history by ID"""
    return db.query(DetectionHistory).filter(
        DetectionHistory.id == history_id,
        DetectionHistory.user_id == user_id
    ).first()


def delete_detection_history(db: Session, history_id: int, user_id: int) -> bool:
    """Delete detection history"""
    history = get_detection_by_id(db, history_id, user_id)
    
    if not history:
        return False
    
    db.delete(history)
    db.commit()
    
    return True


def get_user_detection_count(db: Session, user_id: int) -> int:
    """Get total detection count for user"""
    return db.query(DetectionHistory).filter(
        DetectionHistory.user_id == user_id
    ).count()


def get_user_statistics(db: Session, user_id: int) -> dict:
    """Get detection statistics for user"""
    total_detections = db.query(DetectionHistory).filter(
        DetectionHistory.user_id == user_id
    ).count()
    
    # Get most common diseases
    common_diseases = (
        db.query(
            DetectionHistory.disease_name,
            func.count(DetectionHistory.id).label('count')
        )
        .filter(DetectionHistory.user_id == user_id)
        .group_by(DetectionHistory.disease_name)
        .order_by(desc('count'))
        .limit(5)
        .all()
    )
    
    return {
        "total_detections": total_detections,
        "common_diseases": [
            {"disease": name, "count": count}
            for name, count in common_diseases
        ]
    }