"""Endpoint simple para subir CSV y colocarlo en uploads/csv/raw"""
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from pathlib import Path
import shutil
import sys
import traceback
from typing import Optional

router = APIRouter()

# Base real del backend (sube cuatro niveles hasta la carpeta backend)
BACKEND_BASE = Path(__file__).resolve().parent.parent.parent.parent  # .../backend
RAW_DIR = BACKEND_BASE / "uploads" / "csv" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-csv")
async def upload_csv_file(background_tasks: BackgroundTasks, file: UploadFile = File(...), sync: bool = False):
    print("[UPLOAD] Inicio subida archivo:", file.filename)
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos .csv")
    target_path = RAW_DIR / file.filename
    # Evitar sobreescritura añadiendo sufijo si existe
    counter = 1
    base = target_path.stem
    ext = target_path.suffix
    while target_path.exists():
        target_path = RAW_DIR / f"{base}_{counter}{ext}"
        counter += 1
    try:
        with open(target_path, 'wb') as out:
            shutil.copyfileobj(file.file, out)
        print(f"[UPLOAD] Guardado en {target_path}")
    except Exception as e:
        print("[UPLOAD][ERROR] Falló guardado:", e)
        raise HTTPException(status_code=500, detail=f"Error guardando archivo: {e}")

    def run_process(nombre):
        try:
            print("[PROCESS] Iniciando procesamiento de:", nombre)
            services_dir = Path(__file__).resolve().parent.parent.parent / 'services'
            if str(services_dir) not in sys.path:
                sys.path.insert(0, str(services_dir))
                print("[PROCESS] Añadido services al sys.path")
            from app.services.csv_processor import csv_processor
            resultado = csv_processor.procesar_archivo_especifico(Path(nombre).name)
            print("[PROCESS] Resultado segmentos:", len(resultado) if isinstance(resultado, list) else resultado)
        except Exception as e:
            print("[PROCESS][ERROR]", e)
            traceback.print_exc()

    if sync:
        run_process(target_path)
        return {"message": "Archivo subido y procesado (sync)", "filename": target_path.name, "path": str(target_path)}
    else:
        background_tasks.add_task(run_process, target_path)
        return {"message": "Archivo subido", "filename": target_path.name, "path": str(target_path)}
