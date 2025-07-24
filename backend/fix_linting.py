#!/usr/bin/env python3
"""
Script para arreglar todos los problemas de linting de flake8
"""

import os
import re
import glob

def fix_imports():
    """Elimina imports no utilizados"""
    files_to_fix = [
        "app/api/endpoints/segmentos.py",
        "app/api/process.py", 
        "app/models/orm_models.py",
        "app/schemas/segmento.py",
        "app/services/muestra_service.py",
        "app/services/segmento_service.py",
        "app/services/segmentos_service.py"
    ]
    
    import_fixes = {
        "app/api/endpoints/segmentos.py": [
            ("from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto", 
             "from app.schemas.responses import GeoJSONFeatureCollection")
        ],
        "app/api/process.py": [
            ("from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto",
             "from app.schemas.responses import GeoJSONFeatureCollection")
        ],
        "app/models/orm_models.py": [
            ("from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text",
             "from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey")
        ],
        "app/schemas/segmento.py": [
            ("from typing import List, Optional",
             "from typing import Optional"),
            ("from datetime import datetime",
             "")
        ],
        "app/services/muestra_service.py": [
            ("from app.schemas.muestras import MuestraCreate, Muestra, IndicesMuestraCreate, HuecoMuestraCreate",
             "from app.schemas.muestras import MuestraCreate, Muestra")
        ],
        "app/services/segmento_service.py": [
            ("from app.schemas.segmento import SegmentoCreate, Segmento, GeometriaCreate, IndicesSegmentoCreate, HuecoSegmentoCreate",
             "from app.schemas.segmento import SegmentoCreate, Segmento"),
            ("from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto",
             "from app.schemas.responses import GeoJSONFeatureCollection")
        ],
        "app/services/segmentos_service.py": [
            ("from app.schemas.segmentos import SegmentoCreate, Segmento, GeometriaCreate, IndicesSegmentoCreate, HuecoSegmentoCreate",
             "from app.schemas.segmentos import SegmentoCreate, Segmento"),
            ("from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto",
             "from app.schemas.responses import GeoJSONFeatureCollection")
        ]
    }
    
    for file_path, fixes in import_fixes.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old_import, new_import in fixes:
                content = content.replace(old_import, new_import)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

def fix_whitespace_and_lines():
    """Arregla espacios en blanco y líneas vacías"""
    
    # Buscar todos los archivos Python
    python_files = []
    for root, dirs, files in os.walk("app"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Arreglar líneas
        new_lines = []
        prev_was_function_or_class = False
        
        for i, line in enumerate(lines):
            # Eliminar trailing whitespace
            line = line.rstrip() + '\n'
            
            # Arreglar líneas en blanco con espacios
            if line.strip() == '':
                line = '\n'
            
            # Agregar líneas en blanco antes de funciones/clases
            if (line.startswith('def ') or line.startswith('class ') or 
                line.startswith('async def ')):
                
                # Ver cuántas líneas en blanco hay antes
                blank_lines_before = 0
                j = len(new_lines) - 1
                while j >= 0 and new_lines[j].strip() == '':
                    blank_lines_before += 1
                    j -= 1
                
                # Si no es la primera línea del archivo y no hay suficientes líneas en blanco
                if len(new_lines) > 0 and blank_lines_before < 2:
                    # Eliminar las líneas en blanco existentes
                    while new_lines and new_lines[-1].strip() == '':
                        new_lines.pop()
                    # Agregar exactamente 2 líneas en blanco
                    new_lines.extend(['\n', '\n'])
                
                prev_was_function_or_class = True
            else:
                prev_was_function_or_class = False
            
            new_lines.append(line)
        
        # Agregar 2 líneas en blanco al final de funciones/clases si es necesario
        if new_lines:
            # Eliminar líneas en blanco al final del archivo
            while new_lines and new_lines[-1].strip() == '':
                new_lines.pop()
            
            # Agregar una línea en blanco al final
            new_lines.append('\n')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def fix_long_lines():
    """Arregla líneas demasiado largas"""
    long_line_fixes = {
        "app/core/config.py": [
            ('    POSTGRES_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"',
             '    POSTGRES_URL: str = (\n        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"\n        f"@{POSTGRES_SERVER}/{POSTGRES_DB}"\n    )')
        ],
        "app/services/segmento_service.py": [
            ('from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto',
             'from app.schemas.responses import GeoJSONFeatureCollection')
        ],
        "app/services/segmentos_service.py": [
            ('from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto',
             'from app.schemas.responses import GeoJSONFeatureCollection')
        ],
        "app/services/sensores_service.py": [
            ('        return {"message": f"Datos de sensores procesados correctamente para el segmento {segmento_id}"}',
             '        return {\n            "message": f"Datos de sensores procesados correctamente "\n                      f"para el segmento {segmento_id}"\n        }')
        ]
    }
    
    for file_path, fixes in long_line_fixes.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old_line, new_line in fixes:
                content = content.replace(old_line, new_line)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    print("🔧 Arreglando imports no utilizados...")
    fix_imports()
    
    print("🔧 Arreglando espacios en blanco y líneas vacías...")
    fix_whitespace_and_lines()
    
    print("🔧 Arreglando líneas demasiado largas...")
    fix_long_lines()
    
    print("✅ ¡Arreglos completados!")
