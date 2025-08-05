import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "RecWay")
    API_V1_STR = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY = os.getenv("SECRET_KEY", "recway-secret-key-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:edward123@localhost:5432/recWay_db")
    
    # CORS Configuration
    CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", '["*"]')
    CORS_ORIGINS = ["*"]  # Simplified for now
    
    # Email settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@recway.com")
    EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "RecWay")
    
    # URLs for email links
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    PASSWORD_RESET_URL = f"{FRONTEND_URL}/reset-password"
    EMAIL_VERIFICATION_URL = f"{FRONTEND_URL}/verify-email"

settings = Settings()
