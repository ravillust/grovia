from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class DetectionResult(BaseModel):
    disease_id: str
    disease_name: str
    scientific_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: Optional[str] = None
    symptoms: List[str] = []
    detected_at: datetime

    class Config:
        from_attributes = True


class TreatmentRecommendation(BaseModel):
    disease_id: str
    disease_name: str
    prevention: List[str] = []
    treatment: List[str] = []
    organic_solutions: List[str] = []
    chemical_solutions: List[str] = []
    additional_tips: List[str] = []

    class Config:
        from_attributes = True


class DetectionHistoryCreate(BaseModel):
    disease_id: str
    disease_name: str
    confidence: float
    image_url: str
    timestamp: datetime


class DetectionHistoryResponse(BaseModel):
    history_id: int
    disease_id: str
    disease_name: str
    scientific_name: Optional[str] = None
    confidence: float
    image_url: str
    detected_at: datetime

    class Config:
        from_attributes = True


class DetectionHistoryDetail(BaseModel):
    history_id: int
    disease_id: str
    disease_name: str
    scientific_name: Optional[str] = None
    confidence: float
    image_url: str
    description: Optional[str] = None
    symptoms: List[str] = []
    detected_at: datetime

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    sort: str = Field(default="newest")


class PaginatedResponse(BaseModel):
    items: List[DetectionHistoryResponse]
    pagination: dict