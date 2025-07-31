from datetime import datetime, timedelta, timezone
from typing import Any
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.user import User, AuthToken

router = APIRouter()

def hash_password(password: str) -> str:
    """Simple password hashing for testing"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

@router.post("/register")
def register(
    email: str = Body(...),
    password: str = Body(...),
    full_name: str = Body(None),
    db: Session = Depends(get_db)
):
    """Register a new user - simplified version"""
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create user with correct field names matching DB
    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        country_code='CO',
        is_active=True,
        is_email_verified=True,
        registered_at=datetime.utcnow()
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "message": "User registered successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/login")
def login(
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    """Login user - simplified version"""
    
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last activity
    user.last_activity = datetime.utcnow()
    db.commit()
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "message": "Login successful"
    }

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    """List all users for testing"""
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "registered_at": user.registered_at
        }
        for user in users
    ]
