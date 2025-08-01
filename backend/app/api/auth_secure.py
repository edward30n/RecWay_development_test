"""
Secure Authentication endpoints for RecWay API
Enhanced JWT-based authentication with 30-day token expiration
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, timedelta
import logging

from app.db.session import get_db
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token,
    store_token_in_db,
    revoke_token
)
from app.models.user import User, AuthToken
from app.models.company import Company

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication router
auth_router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# Security scheme for JWT
security = HTTPBearer()

# Helper function for getting current user
def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    token = credentials.credentials
    
    # Verify token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Update last activity
    user.last_activity = datetime.utcnow()
    db.commit()
    
    return user

# Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = True

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    country_code: str = "CO"
    phone: Optional[str] = None
    company_id: Optional[int] = None

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[int] = None
    registered_at: datetime
    last_activity: Optional[datetime] = None
    is_active: bool
    is_email_verified: bool
    country_code: str

@auth_router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user with enhanced security
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Validate company if provided
    if user_data.company_id:
        company = db.query(Company).filter(
            Company.id == user_data.company_id,
            Company.is_active == True
        ).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid company ID"
            )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        country_code=user_data.country_code,
        company_id=user_data.company_id,
        is_active=True,
        is_email_verified=False,
        registered_at=datetime.utcnow(),
        last_activity=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create tokens
    access_token = create_access_token(subject=new_user.id)
    refresh_token = create_refresh_token(subject=new_user.id)
    
    # Store tokens in database
    expires_at = datetime.utcnow() + timedelta(minutes=43200)  # 30 days
    store_token_in_db(db, new_user.id, access_token, expires_at)
    
    logger.info(f"New user registered: {new_user.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=43200 * 60,  # 30 days in seconds
        user={
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "company_id": new_user.company_id,
            "is_email_verified": new_user.is_email_verified
        }
    )

@auth_router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT tokens
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Store tokens in database
    expires_at = datetime.utcnow() + timedelta(minutes=43200)  # 30 days
    store_token_in_db(db, user.id, access_token, expires_at)
    
    # Update last activity
    user.last_activity = datetime.utcnow()
    db.commit()
    
    logger.info(f"User logged in: {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=43200 * 60,  # 30 days in seconds
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "company_id": user.company_id,
            "is_email_verified": user.is_email_verified
        }
    )

@auth_router.post("/refresh-token", response_model=TokenResponse)
def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    # Verify refresh token
    payload = verify_token(refresh_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Store new access token
    expires_at = datetime.utcnow() + timedelta(minutes=43200)  # 30 days
    store_token_in_db(db, user.id, access_token, expires_at)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=43200 * 60,  # 30 days in seconds
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "company_id": user.company_id,
            "is_email_verified": user.is_email_verified
        }
    )

@auth_router.post("/logout")
def logout(
    logout_data: LogoutRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Logout user and revoke tokens
    """
    # Extract access token from header
    access_token = authorization.replace("Bearer ", "")
    
    # Revoke both tokens
    revoke_token(db, access_token)
    revoke_token(db, logout_data.refresh_token)
    
    return {"message": "Successfully logged out"}

@auth_router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Get current authenticated user information
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        company_id=current_user.company_id,
        registered_at=current_user.registered_at,
        last_activity=current_user.last_activity,
        is_active=current_user.is_active,
        is_email_verified=current_user.is_email_verified,
        country_code=current_user.country_code
    )

@auth_router.get("/validate-token")
def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Validate JWT token and return user info
    """
    token = credentials.credentials
    
    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get user
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return {
        "valid": True,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "company_id": user.company_id
        }
    }

@auth_router.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "authentication"
    }
