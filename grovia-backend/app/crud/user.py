from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    try:
        hashed_password = get_password_hash(user.password)
        
        # Generate username from email (part before @)
        username = user.email.split('@')[0]
        
        db_user = User(
            email=user.email,
            username=username,
            name=user.name,
            full_name=user.name,  # Use name as full_name by default
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating user: {str(e)}")


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user"""
    db_user = get_user_by_id(db, user_id)
    
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password
    
    Args:
        db: Database session
        email: User email
        password: Plain password
        
    Returns:
        User if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
    """
    Change user password
    
    Args:
        db: Database session
        user_id: User ID
        old_password: Current password
        new_password: New password
        
    Returns:
        True if password change successful, False otherwise
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
        
    if not verify_password(old_password, user.hashed_password):
        return False
        
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return True


def verify_user_email(db: Session, user_id: int) -> bool:
    """
    Mark user email as verified
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        True if verification successful, False if user not found
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
        
    user.is_verified = True
    db.commit()
    
    return True


def deactivate_user(db: Session, user_id: int) -> bool:
    """
    Deactivate user account
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        True if deactivation successful, False if user not found
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
        
    user.is_active = False
    db.commit()
    
    return True


def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    user = get_user_by_id(db, user_id)
    
    if not user:
        return False
    
    db.delete(user)
    db.commit()
    
    return True