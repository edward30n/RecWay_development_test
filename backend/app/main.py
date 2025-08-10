from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

from app.api.auth_secure import auth_router
from app.core.config import settings
from app.db.session import get_db
import app.models
from app.api.endpoints.upload import router as upload_router
from app.api.endpoints.auto_processing import router as auto_processing_router
from app.services.file_watcher import start_file_watcher, stop_file_watcher
try:
    from app.api.routes.manual_processing import router as manual_processing_router
except ImportError:
    manual_processing_router = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
app.include_router(upload_router, prefix=settings.API_V1_STR + "/files", tags=["files"])
app.include_router(auto_processing_router, prefix=settings.API_V1_STR + "/auto-process", tags=["auto-processing"])
if manual_processing_router:
    app.include_router(manual_processing_router, prefix=settings.API_V1_STR + "/manual-process", tags=["manual-processing"])

# Eventos de aplicación
@app.on_event("startup")
async def startup_event():
    """Eventos que se ejecutan al iniciar la aplicación"""
    logger.info("Iniciando RecWay API...")
    
    # Iniciar file watcher para procesamiento automático
    if start_file_watcher():
        logger.info("✅ File Watcher iniciado correctamente")
    else:
        logger.warning("⚠️ No se pudo iniciar el File Watcher")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos que se ejecutan al cerrar la aplicación"""
    logger.info("Cerrando RecWay API...")
    
    # Detener file watcher
    stop_file_watcher()
    logger.info("✅ File Watcher detenido")

# Countries endpoint (needed by frontend)
@app.get("/api/v1/countries")
def get_countries(db: Session = Depends(get_db)):
    """
    Get list of available countries for frontend signup
    """
    from app.models.user import Country
    
    countries = db.query(Country).order_by(Country.name).all()
    
    # Static phone prefixes mapping since it's not in DB schema
    phone_prefixes = {
        'CO': '+57', 'US': '+1', 'MX': '+52', 'AR': '+54', 'BR': '+55',
        'CL': '+56', 'PE': '+51', 'EC': '+593', 'ES': '+34', 'UK': '+44'
    }
    
    return [
        {
            "code": country.code,
            "name": country.name,
            "phone_prefix": phone_prefixes.get(country.code, "+1")
        }
        for country in countries
    ]

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
