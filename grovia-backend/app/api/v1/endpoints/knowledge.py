from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import disease as disease_crud
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("/diseases", response_model=dict)
async def get_all_diseases(
    search: Optional[str] = Query(None, description="Search by disease name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """
    Get all diseases with optional filters
    """
    
    # Get diseases from database
    diseases = disease_crud.get_all_diseases(
        db=db,
        search=search,
        category=category
    )
    
    # Format response
    diseases_list = []
    for disease in diseases:
        diseases_list.append({
            "disease_id": disease.disease_id,
            "disease_name": disease.disease_name,
            "scientific_name": disease.scientific_name,
            "category": disease.category.value if disease.category else None,
            "severity": disease.severity.value if disease.severity else None,
            "thumbnail": disease.thumbnail
        })
    
    return {
        "success": True,
        "data": diseases_list
    }


@router.get("/diseases/{disease_id}", response_model=dict)
async def get_disease_detail(
    disease_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about specific disease
    """
    
    # Get disease from database
    disease = disease_crud.get_disease_by_id(db, disease_id)
    
    if not disease:
        raise NotFoundError(f"Disease '{disease_id}' not found")
    
    # Parse and format response
    disease_detail = disease_crud.parse_disease_json_fields(disease)
    
    return {
        "success": True,
        "data": disease_detail
    }


@router.get("/categories", response_model=dict)
async def get_disease_categories():
    """
    Get list of disease categories
    """
    
    categories = [
        {"value": "fungal", "label": "Jamur"},
        {"value": "bacterial", "label": "Bakteri"},
        {"value": "viral", "label": "Virus"},
        {"value": "pest", "label": "Hama"}
    ]
    
    return {
        "success": True,
        "data": categories
    }


@router.get("/severity-levels", response_model=dict)
async def get_severity_levels():
    """
    Get list of severity levels
    """
    
    severity_levels = [
        {"value": "high", "label": "Tinggi", "color": "#e53e3e"},
        {"value": "medium", "label": "Sedang", "color": "#d69e2e"},
        {"value": "low", "label": "Rendah", "color": "#38a169"}
    ]
    
    return {
        "success": True,
        "data": severity_levels
    }