# Wrapper simple para usar el código original de main_procesamiento
import sys
from pathlib import Path

services_dir = str(Path(__file__).parent)
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# Se cambia a main_procesamiento como fuente primaria
import main_procesamiento as procesamiento
import algoritmos_busqueda as ab

class CSVProcessor:
    def __init__(self):
        pass
    
    def procesar_archivos_pendientes(self):
        return procesamiento.procesar()
    
    def procesar_archivo_especifico(self, nombre_archivo):
        return procesamiento.procesar_archivo_especifico(nombre_archivo)
    
    def buscar_archivos_por_nombre(self, carpeta, prefijo):
        return ab.buscar_archivos_por_nombre(carpeta, prefijo)
    
    @property
    def carpeta_csv(self):
        return procesamiento.carpeta_csv
    
    @property 
    def carpeta_almacenamiento_csv(self):
        return procesamiento.carpeta_almacenamiento_csv
    
    @property
    def prefijo_busqueda(self):
        return procesamiento.prefijo_busqueda
    
    @property
    def carpeta_archivos_json(self):
        return procesamiento.carpeta_archivos_json
    
    @property
    def carpeta_almacenamiento_json(self):
        return procesamiento.carpeta_almacenamiento_json

csv_processor = CSVProcessor()
