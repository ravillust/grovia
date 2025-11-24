from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime, timezone
from app.database import Base


class DetectionHistory(Base):
    __tablename__ = "detection_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    disease_id = Column(String, nullable=False)
    disease_name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=True)
    confidence = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    symptoms = Column(Text, nullable=True)  # JSON string
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    def __repr__(self):
        return f"<DetectionHistory(id={self.id}, disease={self.disease_name}, confidence={self.confidence})>"