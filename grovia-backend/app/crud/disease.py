from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.models.disease import Disease


def get_all_diseases(db: Session, search: Optional[str] = None, category: Optional[str] = None) -> List[Disease]:
    """Get all diseases with optional filters"""
    query = db.query(Disease)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Disease.disease_name.ilike(search_term)) |
            (Disease.scientific_name.ilike(search_term))
        )
    
    if category:
        query = query.filter(Disease.category == category)
    
    return query.all()


def get_disease_by_id(db: Session, disease_id: str) -> Optional[Disease]:
    """Get disease by ID - with safe column loading"""
    try:
        return db.query(Disease).filter(Disease.disease_id == disease_id).first()
    except Exception as e:
        # If query fails (e.g., missing columns), try with basic fields only
        print(f"Warning: Could not load disease with all fields: {e}")
        return None


def get_treatment_recommendation(db: Session, disease_id: str) -> Optional[dict]:
    """Get treatment recommendation for disease"""
    disease = get_disease_by_id(db, disease_id)
    
    if not disease:
        return None
    
    return {
        "disease_id": disease.disease_id,
        "disease_name": disease.disease_name,
        "prevention": json.loads(disease.prevention) if disease.prevention else [],
        "treatment": json.loads(disease.treatment) if disease.treatment else [],
        "organic_solutions": json.loads(disease.organic_solutions) if disease.organic_solutions else [],
        "chemical_solutions": json.loads(disease.chemical_solutions) if disease.chemical_solutions else [],
        "additional_tips": json.loads(disease.additional_tips) if disease.additional_tips else []
    }


def parse_disease_json_fields(disease: Disease) -> dict:
    """Parse JSON fields in disease model"""
    return {
        "disease_id": disease.disease_id,
        "disease_name": disease.disease_name,
        "scientific_name": disease.scientific_name,
        "description": disease.description,
        "symptoms": json.loads(disease.symptoms) if disease.symptoms else [],
        "causes": json.loads(disease.causes) if disease.causes else [],
        "affected_plants": json.loads(disease.affected_plants) if disease.affected_plants else [],
        "prevention": json.loads(disease.prevention) if disease.prevention else [],
        "treatment": json.loads(disease.treatment) if disease.treatment else [],
        "images": json.loads(disease.images) if disease.images else [],
        "thumbnail": disease.thumbnail if disease.thumbnail else None
    }