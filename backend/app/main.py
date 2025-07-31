from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_secure import auth_router
from app.core.config import settings
# Import all models to ensure they are registered with SQLAlchemy
import app.models  # This will import all models

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="RecWay API with Secure JWT Authentication",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include secure authentication endpoints
app.include_router(auth_router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RecWay API",
        "version": "1.0.0"
    }

@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
