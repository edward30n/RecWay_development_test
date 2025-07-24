from app.api.endpoints import muestras, segmentos, sensores
from fastapi import APIRouter

api_router = APIRouter()

# Incluir todos los routers de endpoints organizados por carpetas
api_router.include_router(segmentos.router)
api_router.include_router(muestras.router)
api_router.include_router(sensores.router)


# Endpoint de información de la API actualizado
@api_router.get("/info")
async def api_info():
    """Información completa sobre los endpoints disponibles de la API RecWay"""
    return {
        "api_name": "RecWay API",
        "version": "2.0.0",
        "description": "API para gestión completa de segmentos de carretera, análisis de calidad y datos de sensores",
        "database_version": "2.0 - Estructura completa con sensores",
        "endpoints": {
            "segmentos": {
                "GET /segmentos/": "Obtener todos los segmentos",
                "GET /segmentos/{id}": "Obtener segmento específico",
                "POST /segmentos/": "Crear nuevo segmento",
                "GET /segmentos/geojson/all": "Obtener segmentos en formato GeoJSON para mapas",
                "GET /segmentos/{id}/geometrias": "Obtener puntos que definen un segmento",
                "GET /segmentos/{id}/indices": "Obtener índices de calidad de un segmento",
                "GET /segmentos/{id}/huecos": "Obtener huecos detectados en un segmento",
            },
            "muestras": {
                "GET /muestras/": "Obtener todas las muestras",
                "GET /muestras/{id}": "Obtener muestra específica con datos relacionados",
                "POST /muestras/": "Crear nueva muestra",
                "GET /muestras/segmento/{id}": "Obtener muestras de un segmento específico",
                "GET /muestras/{id}/indices": "Obtener índices de calidad de una muestra",
                "GET /muestras/{id}/huecos": "Obtener huecos detectados en una muestra",
            },
            "sensores": {
                "GET /sensores/fuentes": "Obtener todas las fuentes de datos de dispositivos",
                "GET /sensores/fuentes/{id}": "Obtener información detallada de una fuente",
                "POST /sensores/fuentes": "Registrar nueva fuente de datos de dispositivo",
                "GET /sensores/registros/fuente/{id}": "Obtener registros de sensores de una fuente",
                "POST /sensores/registros": "Crear nuevo registro de sensores",
                "POST /sensores/registros/bulk": "Crear múltiples registros de sensores",
                "GET /sensores/completos/{id}": "Obtener datos completos de una fuente",
            },
        },
        "nuevas_caracteristicas": [
            "Gestión completa de datos de sensores (acelerómetro, giroscopio, GPS)",
            "Metainformación detallada de dispositivos",
            "Estructura de base de datos optimizada",
            "Endpoints organizados por módulos",
            "Soporte para importación masiva de datos",
            "Campos actualizados en segmentos (nodos X/Y, superficie, ancho, error GPS)",
        ],
    }


# Endpoint de compatibilidad para procesos legacy
@api_router.post("/process")
async def process_legacy():
    """Endpoint de compatibilidad para procesos heredados"""
    return {
        "status": "ok",
        "message": "Endpoint de compatibilidad. Use los nuevos endpoints específicos.",
        "redirect_to": "/api/v1/info",
    }


@api_router.get("/process")
async def get_process_legacy():
    """Endpoint de compatibilidad que redirige a segmentos GeoJSON"""
    return {
        "message": "Este endpoint ha sido movido",
        "new_endpoint": "/api/v1/segmentos/geojson/all",
        "description": "Use el nuevo endpoint para obtener datos GeoJSON",
    }
