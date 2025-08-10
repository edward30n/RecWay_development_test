"""
Endpoints para el procesamiento automático de archivos CSV
"""
from typing import List, Dict
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.csv_processor import csv_processor
from app.services.file_watcher import start_file_watcher, stop_file_watcher, get_file_watcher_status
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/process-pending")
async def process_pending_files(background_tasks: BackgroundTasks):
    """
    Procesar todos los archivos CSV pendientes en la carpeta raw
    """
    try:
        logger.info("Iniciando procesamiento de archivos pendientes")
        
        # Ejecutar procesamiento en background
        def proceso_background():
            return csv_processor.procesar_archivos_pendientes()
        
        background_tasks.add_task(proceso_background)
        
        return {
            "status": "processing_started",
            "message": "El procesamiento de archivos pendientes ha iniciado en segundo plano"
        }
        
    except Exception as e:
        logger.error(f"Error iniciando procesamiento: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error iniciando procesamiento: {str(e)}"
        )

@router.post("/process-file/{filename}")
async def process_specific_file(filename: str, background_tasks: BackgroundTasks):
    """
    Procesar un archivo CSV específico
    """
    try:
        logger.info(f"Iniciando procesamiento de archivo: {filename}")
        
        # Ejecutar procesamiento en background
        def proceso_background():
            return csv_processor.procesar_archivo_especifico(filename)
        
        background_tasks.add_task(proceso_background)
        
        return {
            "status": "processing_started",
            "message": f"El procesamiento del archivo {filename} ha iniciado en segundo plano",
            "filename": filename
        }
        
    except Exception as e:
        logger.error(f"Error iniciando procesamiento de {filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error iniciando procesamiento: {str(e)}"
        )

@router.get("/process-status")
async def get_process_status():
    """
    Obtener estado del procesamiento (archivos pendientes)
    """
    try:
        # Buscar archivos pendientes
        archivos_pendientes = csv_processor.buscar_archivos_por_nombre(
            csv_processor.carpeta_csv, 
            csv_processor.prefijo_busqueda
        )
        
        return {
            "archivos_pendientes": len(archivos_pendientes),
            "archivos": archivos_pendientes,
            "carpeta_raw": csv_processor.carpeta_csv,
            "carpeta_procesados": csv_processor.carpeta_almacenamiento_csv
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estado: {str(e)}"
        )

@router.get("/processed-files")
async def get_processed_files():
    """
    Obtener lista de archivos ya procesados
    """
    try:
        from pathlib import Path
        
        carpeta_procesados = Path(csv_processor.carpeta_almacenamiento_csv)
        carpeta_json = Path(csv_processor.carpeta_archivos_json)
        
        # Listar archivos CSV procesados
        archivos_csv = []
        if carpeta_procesados.exists():
            archivos_csv = [f.name for f in carpeta_procesados.glob("*.csv")]
        
        # Listar archivos JSON generados
        archivos_json = []
        if carpeta_json.exists():
            archivos_json = [f.name for f in carpeta_json.glob("*.json")]
        
        return {
            "archivos_csv_procesados": archivos_csv,
            "archivos_json_generados": archivos_json,
            "total_procesados": len(archivos_csv),
            "total_json": len(archivos_json)
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo archivos procesados: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo archivos procesados: {str(e)}"
        )

@router.delete("/clear-processed")
async def clear_processed_files():
    """
    Limpiar archivos procesados (solo para desarrollo/testing)
    """
    try:
        import shutil
        from pathlib import Path
        
        carpeta_procesados = Path(csv_processor.carpeta_almacenamiento_csv)
        carpeta_json_output = Path(csv_processor.carpeta_archivos_json)
        carpeta_json_storage = Path(csv_processor.carpeta_almacenamiento_json)
        
        archivos_eliminados = 0
        
        # Limpiar CSV procesados
        if carpeta_procesados.exists():
            for archivo in carpeta_procesados.glob("*.csv"):
                archivo.unlink()
                archivos_eliminados += 1
        
        # Limpiar JSON output
        if carpeta_json_output.exists():
            for archivo in carpeta_json_output.glob("*.json"):
                archivo.unlink()
                archivos_eliminados += 1
        
        # Limpiar JSON storage
        if carpeta_json_storage.exists():
            for archivo in carpeta_json_storage.glob("*.json"):
                archivo.unlink()
                archivos_eliminados += 1
        
        return {
            "status": "success",
            "message": f"Se eliminaron {archivos_eliminados} archivos procesados",
            "archivos_eliminados": archivos_eliminados
        }
        
    except Exception as e:
        logger.error(f"Error limpiando archivos: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error limpiando archivos: {str(e)}"
        )

# Endpoints para File Watcher
@router.get("/file-watcher/status")
async def get_file_watcher_status_endpoint():
    """
    Obtener el estado del file watcher
    """
    try:
        status = get_file_watcher_status()
        
        return {
            "status": "active" if status["is_running"] else "inactive",
            "is_running": status["is_running"],
            "watch_folder": status["watch_folder"],
            "observer_alive": status["observer_alive"],
            "message": "File watcher está monitoreando archivos" if status["is_running"] else "File watcher no está activo"
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado del file watcher: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estado: {str(e)}"
        )

@router.post("/file-watcher/start")
async def start_file_watcher_endpoint():
    """
    Iniciar el file watcher manualmente
    """
    try:
        if start_file_watcher():
            return {
                "status": "success",
                "message": "File watcher iniciado correctamente"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="No se pudo iniciar el file watcher"
            )
            
    except Exception as e:
        logger.error(f"Error iniciando file watcher: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error iniciando file watcher: {str(e)}"
        )

@router.post("/file-watcher/stop")
async def stop_file_watcher_endpoint():
    """
    Detener el file watcher manualmente
    """
    try:
        stop_file_watcher()
        return {
            "status": "success",
            "message": "File watcher detenido correctamente"
        }
        
    except Exception as e:
        logger.error(f"Error deteniendo file watcher: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deteniendo file watcher: {str(e)}"
        )
