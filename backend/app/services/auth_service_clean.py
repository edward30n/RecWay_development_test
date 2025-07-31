"""
Authentication services for RecWay
JWT token-based authentication with integrated database
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import text
import secrets
import string

# JWT Configuration
JWT_SECRET_KEY = "recway_secret_key_2025" 
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

class AuthService:
    """Authentication service for RecWay"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self) -> str:
        """Generate random token for auth_tokens"""
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    def create_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT token"""
        payload = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user and return user data with token
        """
        # Get user by email
        query = text("""
            SELECT id, email, full_name, password_hash, is_active, created_at, last_login
            FROM users 
            WHERE email = :email AND is_active = true
        """)
        
        result = self.db.execute(query, {"email": email}).fetchone()
        
        if not result:
            return None
        
        user_dict = dict(result._mapping)
        
        # Verify password
        if not self.verify_password(password, user_dict["password_hash"]):
            return None
        
        # Create auth token record
        auth_token = self.generate_token()
        jwt_token = self.create_jwt_token(user_dict)
        expires_at = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        
        # Insert auth token
        insert_token_query = text("""
            INSERT INTO auth_tokens (user_id, token, expires_at, created_at)
            VALUES (:user_id, :token, :expires_at, :created_at)
        """)
        
        self.db.execute(insert_token_query, {
            "user_id": user_dict["id"],
            "token": auth_token,
            "expires_at": expires_at,
            "created_at": datetime.utcnow()
        })
        
        # Update last login
        update_query = text("""
            UPDATE users SET last_login = :last_login WHERE id = :user_id
        """)
        
        self.db.execute(update_query, {
            "last_login": datetime.utcnow(),
            "user_id": user_dict["id"]
        })
        
        self.db.commit()
        
        # Remove password hash from response
        user_dict.pop("password_hash", None)
        
        return {
            "user": user_dict,
            "token": jwt_token,
            "expires_at": expires_at.isoformat()
        }
    
    def register(self, email: str, password: str, full_name: str, country_code: str = "CO") -> Optional[Dict[str, Any]]:
        """
        Register new user
        """
        # Check if email already exists
        check_query = text("""
            SELECT id FROM users WHERE email = :email
        """)
        
        existing = self.db.execute(check_query, {"email": email}).fetchone()
        
        if existing:
            return None
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Insert new user
        insert_query = text("""
            INSERT INTO users (email, password_hash, full_name, country_code, is_active, created_at)
            VALUES (:email, :password_hash, :full_name, :country_code, true, :created_at)
            RETURNING id, email, full_name, country_code, created_at
        """)
        
        result = self.db.execute(insert_query, {
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name,
            "country_code": country_code,
            "created_at": datetime.utcnow()
        }).fetchone()
        
        if not result:
            return None
        
        user_dict = dict(result._mapping)
        user_id = user_dict["id"]
        
        # Assign default Basic subscription
        subscription_query = text("""
            INSERT INTO user_subscriptions (user_id, plan_id, status, start_date, created_at)
            SELECT :user_id, id, 'active', :start_date, :created_at
            FROM subscription_plans WHERE name = 'Basic'
        """)
        
        self.db.execute(subscription_query, {
            "user_id": user_id,
            "start_date": datetime.utcnow(),
            "created_at": datetime.utcnow()
        })
        
        self.db.commit()
        
        return user_dict
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate authentication token
        """
        # Verify JWT token
        payload = self.verify_jwt_token(token)
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # Get user data
        query = text("""
            SELECT id, email, full_name, country_code, is_active, created_at, last_login
            FROM users 
            WHERE id = :user_id AND is_active = true
        """)
        
        result = self.db.execute(query, {"user_id": user_id}).fetchone()
        
        if not result:
            return None
        
        return dict(result._mapping)
    
    def logout(self, token: str) -> bool:
        """
        Logout user (revoke token)
        """
        payload = self.verify_jwt_token(token)
        if not payload:
            return False
        
        user_id = payload.get("user_id")
        if not user_id:
            return False
        
        # Mark auth tokens as revoked
        query = text("""
            UPDATE auth_tokens 
            SET revoked_at = :revoked_at 
            WHERE user_id = :user_id AND revoked_at IS NULL
        """)
        
        self.db.execute(query, {
            "revoked_at": datetime.utcnow(),
            "user_id": user_id
        })
        
        self.db.commit()
        return True
    
    def get_user_roles(self, user_id: int) -> list:
        """
        Get user roles
        """
        query = text("""
            SELECT r.name, r.description 
            FROM roles r
            JOIN user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = :user_id
        """)
        
        results = self.db.execute(query, {"user_id": user_id}).fetchall()
        
        return [{"name": row.name, "description": row.description} for row in results]
    
    def get_user_subscription(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get active user subscription
        """
        query = text("""
            SELECT sp.name, sp.description, sp.max_projects, sp.max_storage_gb, 
                   us.status, us.start_date, us.end_date
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
