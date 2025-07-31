"""
Simple authentication service for debugging
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
import jwt
import json
from sqlalchemy.orm import Session
from sqlalchemy import text

# Simple JWT config
SECRET_KEY = "debug-key-for-testing-only"
ALGORITHM = "HS256"
EXPIRE_HOURS = 24

# Simple password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SimpleAuthService:
    """Minimal authentication service to debug encoding issues"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_token(self, user_data: Dict[str, Any]) -> str:
        """Create simple JWT token"""
        expire = datetime.utcnow() + timedelta(hours=EXPIRE_HOURS)
        to_encode = {
            "sub": str(user_data["id"]),
            "exp": expire,
            "email": user_data["email"]
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def register(self, email: str, password: str, full_name: str, country_code: str = "CO") -> Optional[Dict[str, Any]]:
        """Simple user registration"""
        try:
            # Check if email exists
            check = text("SELECT id FROM users WHERE email = :email")
            result = self.db.execute(check, {"email": email}).fetchone()
            
            if result:
                return None  # Email already exists
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Insert new user
            query = text("""
                INSERT INTO users (email, password_hash, full_name, country_code, is_active, created_at)
                VALUES (:email, :password_hash, :full_name, :country_code, true, :created_at)
                RETURNING id, email, full_name, country_code, created_at
            """)
            
            now = datetime.utcnow()
            
            user_result = self.db.execute(query, {
                "email": email,
                "password_hash": hashed_password,
                "full_name": full_name,
                "country_code": country_code,
                "created_at": now
            }).fetchone()
            
            if not user_result:
                return None
            
            # Convert to dict
            user_data = dict(user_result._mapping)
            
            # Add subscription
            sub_query = text("""
                INSERT INTO user_subscriptions (user_id, plan_id, status, start_date, created_at)
                SELECT :user_id, id, 'active', :start_date, :created_at
                FROM subscription_plans 
                WHERE name = 'Basic'
            """)
            
            self.db.execute(sub_query, {
                "user_id": user_data["id"],
                "start_date": now,
                "created_at": now
            })
            
            self.db.commit()
            return user_data
            
        except Exception as e:
            self.db.rollback()
            # Print error details for debugging
            print(f"DEBUG ERROR: {str(e)}")
            # Re-raise to let outer exception handler deal with it
            raise e
    
    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Simple login"""
        query = text("""
            SELECT id, email, full_name, password_hash, is_active
            FROM users
            WHERE email = :email AND is_active = true
        """)
        
        result = self.db.execute(query, {"email": email}).fetchone()
        
        if not result:
            return None
            
        user_data = dict(result._mapping)
        
        if not self.verify_password(password, user_data["password_hash"]):
            return None
            
        # Remove password from result
        user_data.pop("password_hash", None)
        
        # Generate token
        token = self.create_token(user_data)
        
        return {
            "user": user_data,
            "token": token,
            "expires_at": (datetime.utcnow() + timedelta(hours=EXPIRE_HOURS)).isoformat()
        }
        
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            
            if not user_id:
                return None
                
            # Get user data
            query = text("""
                SELECT id, email, full_name, country_code, is_active
                FROM users
                WHERE id = :user_id AND is_active = true
            """)
            
            result = self.db.execute(query, {"user_id": user_id}).fetchone()
            
            if not result:
                return None
                
            return dict(result._mapping)
            
        except jwt.PyJWTError:
            return None
            
    def get_user_roles(self, user_id: int) -> list:
        """Get user roles"""
        query = text("""
            SELECT r.name, r.description
            FROM roles r
            JOIN user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = :user_id
        """)
        
        results = self.db.execute(query, {"user_id": user_id}).fetchall()
        return [{"name": row.name, "description": row.description} for row in results] 
        
    def get_user_subscription(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user subscription"""
        query = text("""
            SELECT sp.name, sp.description
            FROM subscription_plans sp
            JOIN user_subscriptions us ON sp.id = us.plan_id
            WHERE us.user_id = :user_id AND us.status = 'active'
            ORDER BY us.created_at DESC
            LIMIT 1
        """)
        
        result = self.db.execute(query, {"user_id": user_id}).fetchone()
        
        if not result:
            return None
            
        return dict(result._mapping)
        
    def logout(self, token: str) -> bool:
        """Simple logout"""
        return True  # Always succeed for testing
