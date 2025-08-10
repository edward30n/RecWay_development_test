# Sistema de Procesamiento Automático de Archivos CSV - RecWay

## Descripción General

El sistema de procesamiento automático procesa archivos CSV que llegan a la carpeta `raw` utilizando los algoritmos de `main_procesamiento.py`. El procesamiento se ejecuta automáticamente cuando se sube un archivo y también puede ser ejecutado manualmente.

## Estructura de Carpetas

```
backend/
├── uploads/
│   ├── csv/
│   │   ├── raw/                    # Archivos CSV recién subidos
│   │   └── processed/              # Archivos CSV ya procesados
│   └── json/
│       ├── output/                 # Resultados JSON para el frontend
│       └── storage/                # Almacenamiento permanente de JSON
├── grafos_archivos5/               # Archivos de grafos para OSM
└── app/
    └── services/
        ├── csv_processor.py        # Servicio de procesamiento
        ├── algoritmos_posicinamiento.py
        └── main_procesamiento.py
```

## Configuración del Sistema

### Variables de Configuración (csv_processor.py)

El sistema está configurado con las siguientes rutas:

- **carpeta_csv**: `uploads/csv/raw` - Donde llegan los archivos CSV
- **prefijo_busqueda**: `"RecWay_"` - Prefijo para identificar archivos a procesar
- **carpeta_archivos_json**: `uploads/json/output` - Salida JSON para frontend
- **carpeta_almacenamiento_csv**: `uploads/csv/processed` - CSV procesados
- **carpeta_almacenamiento_json**: `uploads/json/storage` - JSON almacenados
- **carpeta_grafos**: `grafos_archivos5` - Archivos de grafos OSM

### Procesamiento Automático

El sistema procesa automáticamente archivos que:
1. Estén en la carpeta `uploads/csv/raw`
2. Tengan el prefijo `RecWay_`
3. Sean archivos `.csv`

## Endpoints de la API

### Procesamiento Automático

- **POST** `/api/v1/auto-process/process-pending` - Procesar todos los archivos pendientes
- **POST** `/api/v1/auto-process/process-file/{filename}` - Procesar archivo específico
- **GET** `/api/v1/auto-process/process-status` - Estado del procesamiento
- **GET** `/api/v1/auto-process/processed-files` - Lista de archivos procesados
- **DELETE** `/api/v1/auto-process/clear-processed` - Limpiar archivos procesados

### Upload con Procesamiento Automático

- **POST** `/api/v1/files/upload-csv` - Subir CSV (ahora incluye procesamiento automático)

## Flujo de Procesamiento

1. **Upload**: Un archivo CSV se sube via API a `uploads/csv/raw`
2. **Detección**: El sistema detecta archivos con prefijo `RecWay_`
3. **Procesamiento**: Se ejecuta el algoritmo de `main_procesamiento.py`
4. **Resultados**: Se generan archivos JSON en `uploads/json/output`
5. **Almacenamiento**: El CSV se mueve a `processed` y se guarda JSON en `storage`

## Ejemplo de Uso

### 1. Subir Archivo CSV
```bash
curl -X POST "http://localhost:8000/api/v1/files/upload-csv" \
  -F "file=@RecWay_ejemplo.csv" \
  -F "description=Datos de prueba" \
  -F "category=sensors"
```

### 2. Verificar Estado del Procesamiento
```bash
curl -X GET "http://localhost:8000/api/v1/auto-process/process-status"
```

### 3. Procesar Archivos Pendientes Manualmente
```bash
curl -X POST "http://localhost:8000/api/v1/auto-process/process-pending"
```

### 4. Ver Archivos Procesados
```bash
curl -X GET "http://localhost:8000/api/v1/auto-process/processed-files"
```

## Estructura del Resultado JSON

El procesamiento genera archivos JSON con la siguiente estructura:

```json
[
  {
    "numero": 0,
    "id": "seg_0_100",
    "nombre": "Segmento 1",
    "longitud": 1000.0,
    "tipo": "calle",
    "latitud_origen": 4.6760297,
    "latitud_destino": 4.6762209,
    "longitud_origen": -74.0707725,
    "longitud_destino": -74.0709082,
    "geometria": [
      {
        "latitud": 4.6760297,
        "longitud": -74.0707725
      }
    ],
    "fecha": "2025-01-01T12:00:00",
    "IQR": 2.5,
    "iri": 15.8,
    "IRI_modificado": 3.2,
    "az": 1.8,
    "ax": 2.1,
    "wx": 0.9,
    "huecos": [
      {
        "latitud": 4.6760297,
        "longitud": -74.0707725,
        "magnitud": 1.5,
        "velocidad": 2.3
      }
    ]
  }
]
```

## Logs y Monitoreo

El sistema genera logs detallados que incluyen:
- Archivos detectados para procesamiento
- Progreso del procesamiento
- Errores y excepciones
- Estadísticas de resultados

Los logs se pueden ver en la consola del servidor o configurar para escribir a archivos.

## Dependencias Requeridas

El sistema requiere las siguientes dependencias de Python:

```txt
numpy==2.3.2
pandas==2.3.1
matplotlib==3.10.1
osmnx==2.0.0
networkx==3.4.2
filterpy==1.4.5
```

## Notas Importantes

1. **Grafos OSM**: El sistema requiere archivos de grafos en `grafos_archivos5/`
2. **Prefijo de Archivos**: Solo procesa archivos que comienzan con `RecWay_`
3. **Procesamiento en Background**: El procesamiento se ejecuta en segundo plano
4. **Formato CSV**: El sistema espera un formato específico de columnas GPS
5. **Simulación**: Por ahora usa algoritmos simulados, pendiente integración completa

## Troubleshooting

### Archivo no se procesa
- Verificar que tenga el prefijo `RecWay_`
- Verificar que esté en la carpeta `uploads/csv/raw`
- Revisar logs para errores

### Errores de dependencias
- Instalar dependencias: `pip install -r requirements.txt`
- Verificar versiones de numpy, pandas, osmnx

### Problemas con grafos
- Verificar que existe la carpeta `grafos_archivos5/`
- Verificar archivos de grafos OSM
