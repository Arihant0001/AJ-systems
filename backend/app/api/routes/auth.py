import hashlib
import secrets
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from threading import Lock

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings
from app.db.models import User, PasswordResetToken
from app.db.session import get_db
from app.schemas.auth import LoginIn, SignupIn, TokenOut, ForgotPasswordIn, ResetPasswordIn
from app.utils.email import email_service

router = APIRouter()


# Simple in-memory rate limiter for forgot-password
# In production, use Redis for distributed rate limiting
class RateLimiter:
    def __init__(self, max_requests: int = 3, window_seconds: int = 300):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        with self.lock:
            # Clean old entries
            self.requests[key] = [t for t in self.requests[key] if now - t < self.window_seconds]
            
            if len(self.requests[key]) >= self.max_requests:
                return False
            
            self.requests[key].append(now)
            return True


# Rate limit: 3 requests per 5 minutes per IP
forgot_password_limiter = RateLimiter(max_requests=3, window_seconds=300)


def hash_token(token: str) -> str:
    """Hash token using SHA256 for deterministic lookup"""
    return hashlib.sha256(token.encode()).hexdigest()


def cleanup_expired_tokens(db: Session) -> None:
    """Remove expired and used tokens to keep the table clean"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    db.execute(
        delete(PasswordResetToken).where(
            (PasswordResetToken.expires_at < datetime.now(timezone.utc)) |
            ((PasswordResetToken.used == True) & (PasswordResetToken.created_at < cutoff))
        )
    )


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
def forgot_password(
    payload: ForgotPasswordIn, 
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Initiates password reset flow.
    Always returns 200 OK to prevent email enumeration.
    Rate limited to prevent abuse.
    """
    # Rate limiting by IP address
    client_ip = request.client.host if request.client else "unknown"
    if not forgot_password_limiter.is_allowed(client_ip):
        # Still return success message to prevent enumeration
        return {"message": "If the email exists, a reset link has been sent."}
    
    # Cleanup old tokens periodically
    cleanup_expired_tokens(db)
    
    user = db.scalar(select(User).where(User.email == payload.email))
    if user:
        # Generate secure random token (43 chars, URL-safe)
        token = secrets.token_urlsafe(32)
        token_hash_value = hash_token(token)
        
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.reset_token_expire_minutes)
        
        # Invalidate any previous unused tokens for this user
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used == False
        ).update({"used": True})
        
        # Create new reset token
        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash_value,
            expires_at=expires_at,
        )
        db.add(reset_token)
        db.commit()
        
        # Send email with plain token (hashed version stored in DB)
        email_service.send_password_reset_email(user.email, token)
    
    # Always return same message (prevents email enumeration)
    return {"message": "If the email exists, a reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    """
    Resets user password using a valid reset token.
    Token must be valid, not expired, and not already used.
    """
    # Hash the provided token to look it up
    token_hash_value = hash_token(payload.token)
    
    # Find the reset token (must be valid, not expired, not used)
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Update password with new hash
    user.password_hash = hash_password(payload.new_password)
    
    # Mark token as used (one-time use)
    reset_token.used = True
    
    # Invalidate all other unused tokens for this user
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.id != reset_token.id,
        PasswordResetToken.used == False
    ).update({"used": True})
    
    db.commit()
    
    # Note: JWT tokens remain valid until expiry
    # For immediate session invalidation, implement token blacklisting or use short-lived tokens
    
    return {"message": "Password has been reset successfully"}

