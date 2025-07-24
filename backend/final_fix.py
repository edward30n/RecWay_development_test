#!/usr/bin/env python3
"""
Script final para arreglar los últimos problemas de linting
"""

import os
import re

def final_fixes():
    """Arregla los últimos problemas detectados por flake8"""
    
    # Eliminar imports no utilizados específicos
    fixes = {
        "app/models/orm_models.py": [
            ("from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text",
             "from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey")
        ],
        "app/schemas/segmento.py": [
            ("from typing import List, Optional",
             "from typing import Optional")
        ],
        "app/services/segmento_service.py": [
            ("from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto",
             "from app.schemas.responses import GeoJSONFeatureCollection")
        ],
        "app/services/segmentos_service.py": [
            ("from app.schemas.responses import GeoJSONFeatureCollection, SegmentoCompleto",
             "from app.schemas.responses import GeoJSONFeatureCollection")
        ],
        "app/core/config.py": [
            ('    POSTGRES_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"',
             '    POSTGRES_URL: str = (\n        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"\n        f"@{POSTGRES_SERVER}/{POSTGRES_DB}"\n    )')
        ],
        "app/services/sensores_service.py": [
            ('        return {"message": f"Datos de sensores procesados correctamente para el segmento {segmento_id}"}',
             '        return {\n            "message": (\n                f"Datos de sensores procesados correctamente "\n                f"para el segmento {segmento_id}"\n            )\n        }')
        ]
    }
    
    for file_path, file_fixes in fixes.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old_text, new_text in file_fixes:
                content = content.replace(old_text, new_text)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

def remove_trailing_whitespace_and_fix_spacing():
    """Arregla espacios al final y problemas de espaciado"""
    
    # Buscar todos los archivos Python
    python_files = []
    for root, dirs, files in os.walk("app"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip() + '\n'
            
            # Si es un decorador (@router.get, etc.)
            if line.strip().startswith('@'):
                # Agregar el decorador
                new_lines.append(line)
                i += 1
                
                # Eliminar líneas en blanco después del decorador
                while i < len(lines) and lines[i].strip() == '':
                    i += 1
                
                # Agregar la siguiente línea (que debería ser la función)
                if i < len(lines):
                    next_line = lines[i].rstrip() + '\n'
                    new_lines.append(next_line)
                    i += 1
            else:
                new_lines.append(line)
                i += 1
        
        # Eliminar líneas en blanco al final del archivo
        while new_lines and new_lines[-1].strip() == '':
            new_lines.pop()
        
        # NO agregar línea en blanco al final
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

if __name__ == "__main__":
    print("🔧 Aplicando arreglos finales...")
    final_fixes()
    
    print("🔧 Arreglando espaciado y decoradores...")
    remove_trailing_whitespace_and_fix_spacing()
    
    print("✅ ¡Arreglos finales completados!")
