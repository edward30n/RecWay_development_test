"""
Simple authentication endpoint with minimal dependencies
for testing registration and login without UTF-8 issues
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from ..db.sqlalchemy_db import get_db
from ..models.user import User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple auth router
auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Security scheme
security = HTTPBearer()

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Config
JWT_SECRET = "debugging-secret-key-remove-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

# Models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    country_code: str = "CO"

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None
    token: Optional[str] = None
    expires_at: Optional[str] = None

class RegisterResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

# Helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id: int, email: str) -> str:
    expires = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expires
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Endpoints
@auth_router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Simple registration endpoint"""
    try:
        # Check if email exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        
        if existing_user:
            return RegisterResponse(
                success=False,
                message="Email already registered"
            )
        
        # Hash password
        password_hash = hash_password(request.password)
        
        # Create new user
        now = datetime.utcnow()
        new_user = User(
            email=request.email,
            password_hash=password_hash,
            full_name=request.full_name,
            country_code=request.country_code,
            registered_at=now,
            last_activity=now,
            is_active=True
        )
        
        # Add and commit
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Convert to dict for response
        user_dict = {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "country_code": new_user.country_code,
            "created_at": new_user.registered_at
        }
        
        logger.info(f"New user registered: {request.email}")
        
        return RegisterResponse(
            success=True,
            message="User registered successfully",
            user=user_dict
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@auth_router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Simple login endpoint"""
    try:
        # Get user using SQLAlchemy
        user = db.query(User).filter(
            User.email == request.email, 
            User.is_active == True
        ).first()
        
        if not user:
            return LoginResponse(
                success=False,
                message="User not found or inactive"
            )
            
        # Verify password
        if not verify_password(request.password, user.password_hash):
            return LoginResponse(
                success=False,
                message="Invalid password"
            )
            
        # Generate token
        token = create_token(user.id, user.email)
        
        # Update last activity
        now = datetime.utcnow()
        user.last_activity = now
        db.commit()
        
        # Convert to dict for response
        user_dict = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }
        
        expires_at = (now + timedelta(hours=JWT_EXPIRE_HOURS)).isoformat()
        
        logger.info(f"User logged in: {request.email}")
        
        return LoginResponse(
            success=True,
            message="Login successful",
            user=user_dict,
            token=token,
            expires_at=expires_at
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
