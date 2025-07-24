from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.muestras import Muestra, MuestraCreate
from app.schemas.responses import MuestraCompleta
from app.services.muestra_service import muestra_service

router = APIRouter(prefix="/muestras", tags=["Muestras"])


@router.get("/", response_model=List[Muestra])
async def get_all_muestras():
    """Obtener todas las muestras de datos recolectadas"""
    try:
        return await muestra_service.get_all_muestras()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener muestras: {str(e)}"
        )


@router.get("/{id_muestra}", response_model=MuestraCompleta)
async def get_muestra_completa(id_muestra: int):
    """Obtener una muestra específica con todos sus datos relacionados (índices y huecos)"""
    try:
        muestra = await muestra_service.get_muestra_completa(id_muestra)
        if not muestra:
            raise HTTPException(status_code=404, detail="Muestra no encontrada")
        return muestra
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener muestra: {str(e)}"
        )


@router.post("/", response_model=Muestra)
async def create_muestra(muestra: MuestraCreate):
    """Crear una nueva muestra de datos"""
    try:
        return await muestra_service.create_muestra(muestra)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear muestra: {str(e)}")


@router.get("/segmento/{id_segmento}", response_model=List[Muestra])
async def get_muestras_by_segmento(id_segmento: int):
    """Obtener todas las muestras recolectadas en un segmento específico"""
    try:
        return await muestra_service.get_muestras_by_segmento(id_segmento)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener muestras del segmento: {str(e)}"
        )


@router.get("/{id_muestra}/indices")
async def get_indices_muestra(id_muestra: int):
    """Obtener los índices de calidad calculados para una muestra específica"""
    try:
        indices = await muestra_service.get_indices_by_muestra(id_muestra)
        if not indices:
            raise HTTPException(
                status_code=404, detail="No se encontraron índices para esta muestra"
            )
        return {"muestra_id": id_muestra, "indices": indices}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener índices: {str(e)}"
        )


@router.get("/{id_muestra}/huecos")
async def get_huecos_muestra(id_muestra: int):
    """Obtener los huecos detectados en una muestra específica"""
    try:
        huecos = await muestra_service.get_huecos_by_muestra(id_muestra)
        return {"muestra_id": id_muestra, "huecos": huecos}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener huecos: {str(e)}"
        )
