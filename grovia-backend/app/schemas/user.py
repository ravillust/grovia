from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    password_confirmation: str
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) > 128:
            raise ValueError('Password maksimal 128 karakter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf')
        return v
    
    @validator('password_confirmation')
    def passwords_match(cls, v, values):
        """Validate password confirmation matches"""
        if 'password' in values and v != values['password']:
            raise ValueError('Password tidak sama')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Schema untuk update user"""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema untuk response user"""
    id: int
    email: EmailStr
    name: str
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pydantic v2
        # orm_mode = True  # Gunakan ini jika pakai Pydantic v1


class PasswordChange(BaseModel):
    """Schema untuk ganti password"""
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=128)
    new_password_confirmation: str
    
    @validator('new_password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) > 128:
            raise ValueError('Password maksimal 128 karakter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf')
        return v
    
    @validator('new_password_confirmation')
    def passwords_match(cls, v, values):
        """Validate password confirmation matches"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Password tidak sama')
        return v