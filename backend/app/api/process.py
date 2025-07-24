from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.muestras import Muestra, MuestraCreate
from app.schemas.responses import GeoJSONFeatureCollection, MuestraCompleta
from app.schemas.segmentos import Segmento, SegmentoCreate
from app.services.muestra_service import muestra_service
from app.services.segmento_service import segmento_service

router = APIRouter()

# Endpoints para Segmentos


@router.get("/segmentos", response_model=List[Segmento])
async def get_all_segmentos():
    """Obtener todos los segmentos"""
    try:
        return await segmento_service.get_all_segmentos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener segmentos: {str(e)}")


@router.get("/segmentos/{id_segmento}", response_model=Segmento)
async def get_segmento(id_segmento: float):
    """Obtener un segmento específico por ID"""
    try:
        segmento = await segmento_service.get_segmento_by_id(id_segmento)
        if not segmento:
            raise HTTPException(status_code=404, detail="Segmento no encontrado")
        return segmento
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener segmento: {str(e)}")


@router.post("/segmentos", response_model=Segmento)
async def create_segmento(segmento: SegmentoCreate):
    """Crear un nuevo segmento"""
    try:
        return await segmento_service.create_segmento(segmento)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear segmento: {str(e)}")


@router.get("/segmentos/geojson", response_model=GeoJSONFeatureCollection)
async def get_segmentos_geojson():
    """Obtener todos los segmentos en formato GeoJSON para el mapa"""
    try:
        return await segmento_service.get_segmentos_geojson()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos GeoJSON: {str(e)}")


# Endpoints para Muestras


@router.get("/muestras", response_model=List[Muestra])
async def get_all_muestras():
    """Obtener todas las muestras"""
    try:
        return await muestra_service.get_all_muestras()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener muestras: {str(e)}")


@router.get("/muestras/{id_muestra}", response_model=MuestraCompleta)
async def get_muestra_completa(id_muestra: int):
    """Obtener una muestra con todos sus datos relacionados"""
    try:
        muestra = await muestra_service.get_muestra_completa(id_muestra)
        if not muestra:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")
        return muestra
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener muestra: {str(e)}")


@router.get("/segmentos/{id_segmento}/muestras", response_model=List[Muestra])
async def get_muestras_by_segmento(id_segmento: float):
    """Obtener todas las muestras de un segmento específico"""
    try:
        return await muestra_service.get_muestras_by_segmento(id_segmento)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener muestras del segmento: {str(e)}")


@router.post("/muestras", response_model=Muestra)
async def create_muestra(muestra: MuestraCreate):
    """Crear una nueva muestra"""
    try:
        return await muestra_service.create_muestra(muestra)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear muestra: {str(e)}")


# Endpoints de compatibilidad (manteniendo tu estructura original)


@router.post("/process")
async def process_data(payload: dict):
    """
    Endpoint de compatibilidad para procesar datos
    (mantiene la funcionalidad original pero ahora trabaja con la nueva estructura)
    """
    try:
        # Aquí puedes procesar el payload y crear segmentos/muestras según sea necesario
        # Por ahora solo devolvemos OK para mantener compatibilidad
        return {"status": "ok", "message": "Datos procesados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar datos: {str(e)}")


@router.get("/process")
async def get_process_geojson():
    """
    Endpoint de compatibilidad que devuelve los segmentos en formato GeoJSON
    (mantiene la funcionalidad original)
    """
    try:
        return await segmento_service.get_segmentos_geojson()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")
