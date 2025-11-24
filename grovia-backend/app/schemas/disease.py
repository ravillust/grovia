from pydantic import BaseModel
from typing import List, Optional


class DiseaseBase(BaseModel):
    disease_id: str
    disease_name: str
    scientific_name: str
    category: str
    severity: str


class DiseaseListItem(DiseaseBase):
    thumbnail: Optional[str] = None

    class Config:
        from_attributes = True


class DiseaseDetail(DiseaseBase):
    description: str
    symptoms: List[str]
    causes: List[str]
    affected_plants: List[str]
    prevention: List[str]
    treatment: List[str]
    images: List[str] = []

    class Config:
        from_attributes = True