"""
Script to create database tables
"""
from sqlalchemy import create_engine
from app.core.config import settings
from app.db.session import Base
from app.models import User, Company, AuthToken  # Import all models

def create_tables():
    """Create all database tables"""
    engine = create_engine(str(settings.DATABASE_URI))
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
