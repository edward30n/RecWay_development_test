import os

class Settings:
    PROJECT_NAME = "RecWay"
    API_V1_STR = "/api/v1" 
    SECRET_KEY = "recway-secret-key-change-in-production"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 43200
    REFRESH_TOKEN_EXPIRE_DAYS = 30
    DATABASE_URI = "postgresql://postgres:edward123@localhost:5432/recWay_db"
    CORS_ORIGINS = ["*"]

settings = Settings()
