"""
Security utilities for authentication and authorization
"""
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    # Truncate password to 72 bytes for bcrypt compatibility
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token

    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    try:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt
    except Exception as e:
        raise Exception(f"Error creating access token: {str(e)}")

def verify_token(token: str) -> Optional[str]:
    """
    Verify JWT token

    Args:
        token: JWT token to verify

    Returns:
        Token subject if valid, None otherwise

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid token format"
        )

def hash_verify_token(token: str, salt: str) -> bool:
    """
    Verify a hashed token (for email verification, password reset, etc.)

    Args:
        token: Token to verify
        salt: Salt used in hashing

    Returns:
        True if token is valid, False otherwise
    """
    return pwd_context.verify(token, salt)

def generate_verification_token() -> tuple[str, str]:
    """
    Generate a random token and its hash for email verification

    Returns:
        Tuple of (token, hashed_token)
    """
    import secrets
    token = secrets.token_urlsafe(32)
    hashed_token = pwd_context.hash(token)
    return token, hashed_token
