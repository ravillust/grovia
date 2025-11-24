from sqlalchemy import Column, Integer, String, Text
from datetime import datetime
from app.database import Base
import enum
from sqlalchemy.types import TypeDecorator, String as SQLAlchemyString


class DiseaseCategory(str, enum.Enum):
    FUNGAL = "fungal"
    BACTERIAL = "bacterial"
    VIRAL = "viral"
    PEST = "pest"


class DiseaseSeverity(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EnumAsString(TypeDecorator):
    impl = SQLAlchemyString

    def __init__(self, enum_type):
        super().__init__()
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_type(value)


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(String(100), unique=True, index=True, nullable=False)
    disease_name = Column(String(200), nullable=False)
    scientific_name = Column(String(200), nullable=False)
    # category = Column(EnumAsString(DiseaseCategory), nullable=True)  # Disabled - not in DB
    # severity = Column(EnumAsString(DiseaseSeverity), nullable=True)  # Disabled - not in DB
    description = Column(Text, nullable=False)
    symptoms = Column(Text, nullable=False)  # JSON string
    causes = Column(Text, nullable=True)  # JSON string
    affected_plants = Column(Text, nullable=False)  # JSON string
    prevention = Column(Text, nullable=False)  # JSON string
    treatment = Column(Text, nullable=False)  # JSON string
    organic_solutions = Column(Text, nullable=True)  # JSON string
    chemical_solutions = Column(Text, nullable=True)  # JSON string
    additional_tips = Column(Text, nullable=True)  # JSON string
    thumbnail = Column(String(500), nullable=True)
    images = Column(Text, nullable=True)  # JSON string

    def __repr__(self):
        return f"<Disease(id={self.disease_id}, name={self.disease_name})>"