"""
Simplified main application for authentication testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.minimal_auth import auth_router
from app.core.config import settings
from app.db.sqlalchemy_db import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Test",
    description="Simplified authentication for testing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)


@app.get("/")
async def root():
    """API health check"""
    return {
        "message": f"{settings.PROJECT_NAME} test server is running",
        "version": "1.0.0",
        "docs_url": "/docs",
    }


@app.get("/health")
async def health_check():
    """Database connection test"""
    try:
        # Test database connection
        from sqlalchemy.orm import Session
        from app.db.sqlalchemy_db import SessionLocal
        
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT 1")).fetchone()
            db_status = "connected" if result else "error"
        finally:
            db.close()
            
        return {
            "status": "healthy", 
            "app": settings.PROJECT_NAME, 
            "version": "1.0.0",
            "database": db_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "app": settings.PROJECT_NAME,
            "version": "1.0.0", 
            "error": str(e)
        }
