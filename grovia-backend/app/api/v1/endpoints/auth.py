from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
import secrets
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import logging
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, PasswordChange
from app.schemas.token import LoginRequest, LoginResponse, Token
from app.crud import user as user_crud
from app.core.security import create_access_token
from app.dependencies import get_current_active_user
from app.models.user import User
from pydantic import BaseModel, EmailStr
from google.oauth2 import id_token
from google.auth.transport import requests


# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=getattr(settings, 'MAIL_STARTTLS', True),
    MAIL_SSL_TLS=getattr(settings, 'MAIL_SSL_TLS', False),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

router = APIRouter()
logger = logging.getLogger(__name__)


# Schemas for Forgot Password
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    email: EmailStr
    new_password: str


# Schema for Google Sign In
class GoogleSignInRequest(BaseModel):
    token: str  # Google ID Token from frontend


@router.get("/verify-email")
async def verify_email(token: str, email: str, db: Session = Depends(get_db)):
    """
    Verify user email using token (demo: token not checked, just email)
    """
    user = user_crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        # Sudah diverifikasi, redirect ke login dengan pesan sukses
        return RedirectResponse(url="http://localhost:5173/login?verified=true")
    # For demo, skip token check. In production, save and check token!
    user.is_verified = True
    db.commit()
    db.refresh(user)
    # Redirect ke login dengan pesan sukses
    return RedirectResponse(url="http://localhost:5173/login?verified=true")


@router.post("/resend-verification", response_model=dict)
async def resend_verification(email_data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Resend verification email to user
    """
    try:
        logger.info(f"Attempting to resend verification email to: {email_data.email}")

        # Check if user exists
        user = user_crud.get_user_by_email(db, email=email_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if already verified
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )

        # Generate new verification token
        verify_token = secrets.token_urlsafe(32)

        # Build verification link
        verify_link = f"http://localhost:8000/api/v1/auth/verify-email?token={verify_token}&email={user.email}"

        # Send verification email
        email_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #16a34a;">Verifikasi Email Grovia</h2>
            <p>Halo {user.name},</p>
            <p>Anda meminta untuk mengirim ulang email verifikasi. Klik tombol di bawah ini untuk verifikasi akun Anda:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href='{verify_link}' style='display:inline-block;padding:14px 28px;background:#16a34a;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;'>
                    Verifikasi Email
                </a>
            </div>
            <p style="color: #64748b; font-size: 14px;">Atau copy link berikut ke browser Anda:</p>
            <p style="color: #64748b; font-size: 12px; word-break: break-all;">{verify_link}</p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
            <p style="color: #94a3b8; font-size: 12px;">Jika Anda tidak meminta email ini, abaikan pesan ini.</p>
        </div>
        """
        
        message = MessageSchema(
            subject="Grovia - Email Verification",
            recipients=[user.email],
            body=email_body,
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)

        logger.info(f"Verification email resent successfully to: {user.email}")
        return {
            "success": True,
            "message": "Verification email sent successfully"
        }
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Resend verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )


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

        # Generate verification token (simple random string)
        verify_token = secrets.token_urlsafe(32)

        # Build verification link (adjust domain as needed)
        verify_link = f"http://localhost:8000/api/v1/auth/verify-email?token={verify_token}&email={user.email}"

        # Send verification email (tombol HTML)
        email_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #16a34a;">Welcome to Grovia!</h2>
            <p>Halo {user.name},</p>
            <p>Terima kasih telah mendaftar di Grovia. Klik tombol di bawah ini untuk verifikasi akun Anda:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href='{verify_link}' style='display:inline-block;padding:14px 28px;background:#16a34a;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;'>
                    Verifikasi Email
                </a>
            </div>
            <p style="color: #64748b; font-size: 14px;">Atau copy link berikut ke browser Anda:</p>
            <p style="color: #64748b; font-size: 12px; word-break: break-all;">{verify_link}</p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
            <p style="color: #94a3b8; font-size: 12px;">Jika Anda tidak mendaftar di Grovia, abaikan email ini.</p>
        </div>
        """
        
        message = MessageSchema(
            subject="Grovia - Email Verification",
            recipients=[user.email],
            body=email_body,
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)

        logger.info(f"User registered successfully with id: {user.id}, verification email sent.")
        return {
            "success": True,
            "data": {
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "verification_link": verify_link
            }
        }
    except HTTPException as e:
        raise
    except Exception as e:
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

        # Check if user is verified
        if not user.is_verified:
            logger.warning(f"User not verified: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Akun belum diverifikasi. Silakan cek email untuk aktivasi."
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

        # Create access token
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


@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset - send email with reset link
    """
    try:
        # Log untuk debug
        logger.info(f"[INFO] Forgot password request received for: {request.email}")
        logger.info(f"[INFO] Request headers: {request.headers if hasattr(request, 'headers') else 'N/A'}")
        
        # Check if user exists
        user = user_crud.get_user_by_email(db, email=request.email)
        
        # Always return success to prevent email enumeration
        if not user:
            logger.warning(f"[WARN] Password reset requested for non-existent email: {request.email}")
            return {
                "success": True,
                "message": "If the email exists, a reset link has been sent"
            }
        
        logger.info(f"[SUCCESS] User found: {user.name} (ID: {user.id})")
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store token and expiry in user record
        user.reset_token = reset_token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        
        logger.info(f"[SUCCESS] Token generated and saved for user: {user.email}")
        
        # Build reset link - now points to login page with token parameters
        reset_link = f"http://localhost:5173/login?token={reset_token}&email={user.email}"
        
        # Send reset email
        email_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #0f172a;">Reset Your Password</h2>
            <p>Halo {user.name},</p>
            <p>Kami menerima permintaan untuk mereset password akun Anda di Grovia.</p>
            <p>Klik tombol di bawah ini untuk mereset password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href='{reset_link}' style='display:inline-block;padding:14px 28px;background:#0f172a;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;'>
                    Reset Password
                </a>
            </div>
            <p style="color: #64748b; font-size: 14px;">Atau copy link berikut ke browser Anda:</p>
            <p style="color: #64748b; font-size: 12px; word-break: break-all;">{reset_link}</p>
            <p style="color: #ef4444; font-size: 14px; margin-top: 20px;">[WARNING] Link ini akan kadaluarsa dalam 1 jam.</p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
            <p style="color: #94a3b8; font-size: 12px;">Jika Anda tidak meminta reset password, abaikan email ini.</p>
        </div>
        """
        
        message = MessageSchema(
            subject="Grovia - Reset Password Request",
            recipients=[user.email],
            body=email_body,
            subtype="html"
        )
        
        fm = FastMail(conf)
        logger.info(f"[INFO] Attempting to send email to: {user.email}")
        await fm.send_message(message)
        
        logger.info(f"[SUCCESS] Password reset email successfully sent to: {user.email}")
        
        return {
            "success": True,
            "message": "If the email exists, a reset link has been sent"
        }
        
    except Exception as e:
        logger.error(f"[ERROR] Error in forgot password: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process password reset request"
        )


@router.post("/reset-password", response_model=dict)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using token from email
    """
    try:
        logger.info(f"Password reset attempt for email: {request.email}")
        
        # Find user and verify token
        user = user_crud.get_user_by_email(db, email=request.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if token matches and not expired
        if not user.reset_token or user.reset_token != request.token:
            logger.warning(f"Invalid reset token for: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        if not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
            logger.warning(f"Expired reset token for: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )
        
        # Update password
        from app.core.security import get_password_hash
        user.hashed_password = get_password_hash(request.new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        
        logger.info(f"Password reset successful for: {request.email}")
        
        return {
            "success": True,
            "message": "Password has been reset successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in reset password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
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


@router.post("/google-signin", response_model=dict)
async def google_signin(
    request: GoogleSignInRequest,
    db: Session = Depends(get_db)
):
    """
    Sign in or register user with Google OAuth
    """
    try:
        logger.info("[GOOGLE] Google Sign-In attempt received")
        
        # Verify the Google token
        try:
            idinfo = id_token.verify_oauth2_token(
                request.token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            # Check if token is issued by Google
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
                
            # Get user info from Google token
            google_user_id = idinfo['sub']
            email = idinfo.get('email')
            name = idinfo.get('name', email.split('@')[0])
            email_verified = idinfo.get('email_verified', False)
            
            logger.info(f"[SUCCESS] Google token verified for email: {email}")
            
        except ValueError as e:
            logger.error(f"[ERROR] Invalid Google token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
        
        # Check if user exists
        user = user_crud.get_user_by_email(db, email=email)
        
        if user:
            # User exists, log them in
            logger.info(f"Existing user logging in with Google: {email}")
            
            # Update verification status if Google account is verified
            if email_verified and not user.is_verified:
                user.is_verified = True
                db.commit()
                db.refresh(user)
                logger.info(f"User {email} verified via Google")
        else:
            # New user, create account
            logger.info(f"Creating new user via Google Sign-In: {email}")
            
            # Create user without password (Google-authenticated)
            user_data = UserCreate(
                email=email,
                name=name,
                password=secrets.token_urlsafe(32)  # Random password, won't be used
            )
            
            user = user_crud.create_user(db, user=user_data)
            
            # Mark as verified since Google verified the email
            if email_verified:
                user.is_verified = True
                db.commit()
                db.refresh(user)
        
        # Create access token
        access_token = create_access_token(str(user.id))
        
        logger.info(f"[SUCCESS] Google Sign-In successful for: {email}")
        
        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Error in Google Sign-In: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sign in with Google"
        )


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
    Change user password (for logged in users)
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
