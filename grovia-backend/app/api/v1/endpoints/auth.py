from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from app.database import get_db

logger = logging.getLogger(__name__)
from app.schemas.user import UserCreate, UserResponse, PasswordChange
from app.schemas.token import LoginRequest, LoginResponse, Token
from app.crud import user as user_crud
from app.core.security import create_access_token
from app.dependencies import get_current_active_user
from app.models.user import User
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user
    """
    try:
        logger.info(f"Attempting to register user with email: {user_data.email}")

        # Check if user already exists
        existing_user = user_crud.get_user_by_email(db, email=user_data.email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create user
        logger.info("Creating new user record")
        user = user_crud.create_user(db, user=user_data)

        logger.info(f"User registered successfully with id: {user.id}")
        return {
            "success": True,
            "data": {
                "user_id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log any other errors
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and return access token
    """
    try:
        logger.info(f"Login attempt for email: {login_data.email}")

        # Check if user exists
        user = user_crud.get_user_by_email(db, email=login_data.email)
        if not user:
            logger.warning(f"User not found: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Check password
        from app.core.security import verify_password
        if not verify_password(login_data.password, user.hashed_password):
            logger.warning(f"Password verification failed for: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        logger.info(f"User authenticated successfully: {user.id}")

        # Create simple access token
        access_token = create_access_token(str(user.id))

        logger.info(f"Access token created successfully for user: {user.id}")

        # Prepare user data safely
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }

        # Add created_at safely
        if hasattr(user, 'created_at') and user.created_at:
            try:
                user_data["created_at"] = user.created_at.isoformat()
            except Exception as e:
                logger.warning(f"Error formatting created_at: {e}")
                user_data["created_at"] = str(user.created_at)

        return {
            "success": True,
            "data": {
                "token": access_token,
                "user": user_data
            }
        }
    except HTTPException as e:
        logger.error(f"HTTP Exception in login: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )


@router.post("/logout", response_model=dict)
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout user (client should delete token)
    """
    return {
        "success": True,
        "message": "Successfully logged out"
    }


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information
    """
    try:
        logger.info(f"Getting user info for user ID: {current_user.id}")
        return {
            "success": True,
            "data": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
                "is_active": current_user.is_active,
                "created_at": current_user.created_at.isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting user info: {str(e)}"
        )


@router.put("/profile", response_model=dict)
async def update_profile(
    user_update: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile
    """
    updated_user = user_crud.update_user(db, current_user.id, user_update)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "success": True,
        "data": {
            "id": updated_user.id,
            "email": updated_user.email,
            "name": updated_user.name
        }
    }


@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    success = user_crud.change_password(
        db,
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    return {
        "success": True,
        "message": "Password changed successfully"
    }


@router.get("/debug/user/{email}")
async def debug_get_user(email: str, db: Session = Depends(get_db)):
    """Debug endpoint to check user data"""
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        return {"error": "User not found"}

    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "is_active": user.is_active,
        "has_password": bool(user.hashed_password),
        "password_length": len(user.hashed_password) if user.hashed_password else 0
    }


@router.get("/debug/users")
async def debug_get_all_users(db: Session = Depends(get_db)):
    """Debug endpoint to see all registered users"""
    try:
        users = db.query(User).all()
        return {
            "success": True,
            "data": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.isoformat()
                }
                for user in users
            ],
            "total": len(users)
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/debug/test-insert")
async def debug_test_insert(db: Session = Depends(get_db)):
    """Debug - Test direct insert and select"""
    from sqlalchemy import text

    try:
        # Direct SQL insert
        result = db.execute(text("INSERT INTO users (email, name, hashed_password, is_active, is_verified, created_at) VALUES ('debug@test.com', 'Debug User', 'hashed', true, false, NOW()) RETURNING id, email, name"))
        db.commit()

        inserted = result.fetchone()

        # Immediate select
        select_result = db.execute(text("SELECT COUNT(*) FROM users")).fetchone()

        return {
            "success": True,
            "inserted": {
                "id": inserted[0],
                "email": inserted[1],
                "name": inserted[2]
            } if inserted else None,
            "total_count": select_result[0] if select_result else 0
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/debug/connection-info")
async def debug_connection_info(db: Session = Depends(get_db)):
    """Debug - Get connection and transaction info"""
    from sqlalchemy import text
    try:
        conn_info = db.execute(text("SELECT current_database(), current_user")).fetchone()
        tx_info = db.execute(text("SELECT txid_current()")).fetchone()
        return {
            "success": True,
            "database": conn_info[0],
            "user": conn_info[1],
            "transaction_id": tx_info[0]
        }
    except Exception as e:
        return {"error": str(e)}
