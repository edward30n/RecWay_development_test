from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.schemas.responses import DatosSensoresCompletos
from app.schemas.sensores import (FuenteDatosDispositivo,
                                  FuenteDatosDispositivoCreate,
                                  RegistroSensores, RegistroSensoresCreate)
from app.services.sensores_service import sensores_service

router = APIRouter(prefix="/sensores", tags=["Sensores y Dispositivos"])


# Endpoints para Fuentes de Datos de Dispositivos
@router.get("/fuentes", response_model=List[FuenteDatosDispositivo])
async def get_all_fuentes():
    """Obtener todas las fuentes de datos de dispositivos registradas"""
    try:
        return await sensores_service.get_all_fuentes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener fuentes: {str(e)}")


@router.get("/fuentes/{id_fuente}", response_model=FuenteDatosDispositivo)
async def get_fuente(id_fuente: int):
    """Obtener información detallada de una fuente de datos específica"""
    try:
        fuente = await sensores_service.get_fuente_by_id(id_fuente)
        if not fuente:
            raise HTTPException(status_code=404, detail="Fuente de datos no encontrada")
        return fuente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener fuente: {str(e)}")


@router.post("/fuentes", response_model=FuenteDatosDispositivo)
async def create_fuente(fuente: FuenteDatosDispositivoCreate):
    """Registrar una nueva fuente de datos de dispositivo"""
    try:
        return await sensores_service.create_fuente(fuente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear fuente: {str(e)}")


# Endpoints para Registros de Sensores
@router.get("/registros/fuente/{id_fuente}", response_model=List[RegistroSensores])
async def get_registros_by_fuente(
    id_fuente: int, limit: Optional[int] = Query(1000, description="Número máximo de registros a retornar")
):
    """Obtener registros de sensores de una fuente específica"""
    try:
        return await sensores_service.get_registros_by_fuente(id_fuente, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener registros: {str(e)}")


@router.post("/registros", response_model=RegistroSensores)
async def create_registro(registro: RegistroSensoresCreate):
    """Crear un nuevo registro de datos de sensores"""
    try:
        return await sensores_service.create_registro(registro)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear registro: {str(e)}")


@router.get("/completos/{id_fuente}", response_model=DatosSensoresCompletos)
async def get_datos_completos(id_fuente: int):
    """Obtener datos completos de una fuente (información del dispositivo + registros de sensores)"""
    try:
        datos = await sensores_service.get_datos_completos(id_fuente)
        if not datos:
            raise HTTPException(status_code=404, detail="Fuente de datos no encontrada")
        return datos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos completos: {str(e)}")


# Endpoint para bulk insert de registros (útil para importación masiva)
@router.post("/registros/bulk")
async def create_registros_bulk(registros: List[RegistroSensoresCreate]):
    """Crear múltiples registros de sensores en una sola operación"""
    try:
        created_registros = []
        for registro in registros:
            created_registro = await sensores_service.create_registro(registro)
            created_registros.append(created_registro)

        return {
            "success": True,
            "message": f"Se crearon {len(created_registros)} registros exitosamente",
            "count": len(created_registros),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear registros en bulk: {str(e)}")
