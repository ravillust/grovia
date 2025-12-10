"""
Model untuk menyimpan riwayat deteksi penyakit tanaman
File: app/models/detection_history.py
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class DetectionHistory(Base):
    """
    Model untuk menyimpan history deteksi penyakit pada tanaman
    """
    __tablename__ = "detection_history"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key ke User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Disease Information - Semua String dengan panjang eksplisit
    disease_id = Column(String(100), nullable=False)
    disease_name = Column(String(150), nullable=False)
    scientific_name = Column(String(200), nullable=True)
    
    # Detection Results
    confidence = Column(Float, nullable=False)
    image_url = Column(String(500), nullable=False)
    
    # Additional Information - TEXT untuk konten panjang
    description = Column(String(5000), nullable=True)
    symptoms = Column(String(5000), nullable=True)  # JSON string
    
    # Timestamp
    detected_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        index=True
    )
    
    # Relationship (uncomment jika diperlukan)
    # user = relationship("User", back_populates="detection_histories")
    
    def __repr__(self):
        return f"<DetectionHistory(id={self.id}, disease={self.disease_name}, confidence={self.confidence:.2f})>"
    
    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "disease_id": self.disease_id,
            "disease_name": self.disease_name,
            "scientific_name": self.scientific_name,
            "confidence": round(self.confidence, 2),
            "image_url": self.image_url,
            "description": self.description,
            "symptoms": self.symptoms,
            "detected_at": self.detected_at.isoformat() if self.detected_at else None
        }