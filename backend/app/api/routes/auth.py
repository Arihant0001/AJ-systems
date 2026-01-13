import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings
from app.db.models import User, PasswordResetToken
from app.db.session import get_db
from app.schemas.auth import LoginIn, SignupIn, TokenOut, ForgotPasswordIn, ResetPasswordIn
from app.utils.email import email_service

router = APIRouter()


def hash_token(token: str) -> str:
    """Hash token using SHA256 for deterministic lookup"""
    return hashlib.sha256(token.encode()).hexdigest()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=TokenOut)
def signup(payload: SignupIn, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(payload: ForgotPasswordIn, db: Session = Depends(get_db)):
    """
    Initiates password reset flow.
    Always returns 200 OK to prevent email enumeration.
    """
    user = db.scalar(select(User).where(User.email == payload.email))
    if user:
        # Generate secure random token
        token = secrets.token_urlsafe(32)
        token_hash_value = hash_token(token)
        
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        # Invalidate any previous unused tokens for this user
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used == False
        ).update({"used": True})
        
        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash_value,
            expires_at=expires_at,
        )
        db.add(reset_token)
        db.commit()
        
        # Send email with plain token
        email_service.send_password_reset_email(user.email, token)
    
    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    """
    Resets user password using a valid reset token.
    """
    # Hash the provided token to look it up
    token_hash_value = hash_token(payload.token)
    
    # Find the reset token
    reset_token = db.scalar(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash_value,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.now(timezone.utc)
        )
    )
    
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Get the user
    user = db.get(User, reset_token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    user.password_hash = hash_password(payload.new_password)
    
    # Mark token as used
    reset_token.used = True
    
    db.commit()
    
    return {"message": "Password has been reset successfully"}

