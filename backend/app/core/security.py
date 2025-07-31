from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
import hmac
import json
import base64

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using simple SHA256."""
    # Simple hash for now - in production use bcrypt
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password using simple SHA256."""
    # Simple hash for now - in production use bcrypt
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(subject: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a simple access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    payload = {"exp": expire.timestamp(), **subject}
    # Simple token encoding - in production use JWT properly
    token_data = json.dumps(payload)
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        token_data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return base64.b64encode(f"{token_data}.{signature}".encode()).decode()

def create_refresh_token(subject: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a simple refresh token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {"exp": expire.timestamp(), **subject, "type": "refresh"}
    # Simple token encoding - in production use JWT properly
    token_data = json.dumps(payload)
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        token_data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return base64.b64encode(f"{token_data}.{signature}".encode()).decode()

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a simple token."""
    try:
        decoded = base64.b64decode(token.encode()).decode()
        token_data, signature = decoded.rsplit('.', 1)
        
        # Verify signature
        expected_signature = hmac.new(
            settings.SECRET_KEY.encode(),
            token_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return None
        
        payload = json.loads(token_data)
        
        # Check expiration
        if payload.get("exp", 0) < datetime.now(timezone.utc).timestamp():
            return None
            
        return payload
    except:
        return None

def get_user_from_token(db: Session, token: str) -> Optional[User]:
    """Get user from token."""
    payload = verify_token(token)
    if payload is None:
        return None
    
    user_id = payload.get("sub")
    if user_id is None:
        return None
    
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user
