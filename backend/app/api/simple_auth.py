"""
Simple authentication endpoints for debugging
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import logging

from ..core.database import get_db
from ..services.simple_auth import SimpleAuthService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication router
auth_router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# Security scheme for JWT
security = HTTPBearer()

# Pydantic models
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

class ValidateResponse(BaseModel):
    success: bool
    user: Optional[dict] = None
    roles: Optional[list] = None
    subscription: Optional[dict] = None

# Dependencies
def get_auth_service(db: Session = Depends(get_db)) -> SimpleAuthService:
    """Get simple auth service"""
    return SimpleAuthService(db)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: SimpleAuthService = Depends(get_auth_service)
):
    """Get current user"""
    token = credentials.credentials
    user_data = auth_service.validate_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user_data

# Register endpoint
@auth_router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    auth_service: SimpleAuthService = Depends(get_auth_service)
):
    """Register new user"""
    try:
        # Print for debugging
        print(f"DEBUG: Processing registration for {request.email}")
        
        result = auth_service.register(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            country_code=request.country_code
        )
        
        if not result:
            return RegisterResponse(
                success=False,
                message="Email already registered"
            )
        
        logger.info(f"New user registered: {request.email}")
        
        return RegisterResponse(
            success=True,
            message="User registered successfully",
            user=result
        )
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        print(f"DEBUG EXCEPTION: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Login endpoint
@auth_router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    auth_service: SimpleAuthService = Depends(get_auth_service)
):
    """Login user"""
    try:
        result = auth_service.login(request.email, request.password)
        
        if not result:
            return LoginResponse(
                success=False,
                message="Incorrect email or password"
            )
        
        logger.info(f"User authenticated: {request.email}")
        
        return LoginResponse(
            success=True,
            message="Login successful",
            user=result["user"],
            token=result["token"],
            expires_at=result["expires_at"]
        )
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Validate token endpoint
@auth_router.get("/validate", response_model=ValidateResponse)
async def validate_token(
    current_user: dict = Depends(get_current_user),
    auth_service: SimpleAuthService = Depends(get_auth_service)
):
    """Validate token"""
    try:
        roles = auth_service.get_user_roles(current_user["id"])
        subscription = auth_service.get_user_subscription(current_user["id"])
        
        return ValidateResponse(
            success=True,
            user=current_user,
            roles=roles,
            subscription=subscription
        )
        
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Get user info endpoint
@auth_router.get("/me")
async def get_user_info(
    current_user: dict = Depends(get_current_user),
    auth_service: SimpleAuthService = Depends(get_auth_service)
):
    """Get user info"""
    try:
        roles = auth_service.get_user_roles(current_user["id"])
        subscription = auth_service.get_user_subscription(current_user["id"])
        
        return {
            "success": True,
            "user": current_user,
            "roles": roles,
            "subscription": subscription
        }
        
    except Exception as e:
        logger.error(f"User info error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Logout endpoint
@auth_router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: SimpleAuthService = Depends(get_auth_service)
):
    """Logout user"""
    try:
        token = credentials.credentials
        success = auth_service.logout(token)
        
        return {"success": True, "message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
