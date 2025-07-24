from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto
from app.schemas.segmentos import Segmento, SegmentoCreate
from app.services.segmentos_service import segmento_service

router = APIRouter(prefix="/segmentos", tags=["Segmentos"])


@router.get("/", response_model=List[Segmento])
async def get_all_segmentos():
    """Obtener todos los segmentos de carretera"""
    try:
        return await segmento_service.get_all_segmentos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener segmentos: {str(e)}")


@router.get("/{id_segmento}", response_model=Segmento)
async def get_segmento(id_segmento: int):
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


@router.post("/", response_model=Segmento)
async def create_segmento(segmento: SegmentoCreate):
    """Crear un nuevo segmento de carretera"""
    try:
        return await segmento_service.create_segmento(segmento)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear segmento: {str(e)}")


@router.get("/geojson/all", response_model=GeoJSONFeatureCollection)
async def get_segmentos_geojson():
    """Obtener todos los segmentos en formato GeoJSON para visualización en mapas"""
    try:
        return await segmento_service.get_segmentos_geojson()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos GeoJSON: {str(e)}")


@router.get("/{id_segmento}/geometrias")
async def get_geometrias_segmento(id_segmento: int):
    """Obtener las geometrías (puntos) que definen un segmento"""
    try:
        geometrias = await segmento_service.get_geometrias_by_segmento(id_segmento)
        return {"segmento_id": id_segmento, "geometrias": geometrias}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener geometrías: {str(e)}")


@router.get("/{id_segmento}/indices")
async def get_indices_segmento(id_segmento: int):
    """Obtener los índices de calidad calculados para un segmento"""
    try:
        indices = await segmento_service.get_indices_by_segmento(id_segmento)
        if not indices:
            raise HTTPException(status_code=404, detail="No se encontraron índices para este segmento")
        return {"segmento_id": id_segmento, "indices": indices}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener índices: {str(e)}")


@router.get("/{id_segmento}/huecos")
async def get_huecos_segmento(id_segmento: int):
    """Obtener los huecos detectados en un segmento"""
    try:
        huecos = await segmento_service.get_huecos_by_segmento(id_segmento)
        return {"segmento_id": id_segmento, "huecos": huecos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener huecos: {str(e)}")
