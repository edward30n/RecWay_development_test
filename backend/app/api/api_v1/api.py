from fastapi import APIRouter

from app.api.endpoints import auth

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Health check endpoint
@api_router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "RecWay API is running"}
