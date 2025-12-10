from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    username = Column(String(255), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reset_token = Column(String(255), nullable=True, index=True)
    reset_token_expires = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, is_verified={self.is_verified})>"