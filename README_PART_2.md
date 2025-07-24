#### 📊 app/schemas/ - Modelos de Datos Pydantic

**Patrón de Diseño Implementado:**
```python
# Jerarquía de schemas por entidad:
# Base → Create → Update → Response

# Ejemplo: Segmentos
SegmentoBase      # Campos comunes
├── SegmentoCreate    # Para POST requests
├── SegmentoUpdate    # Para PUT/PATCH requests  
└── SegmentoResponse  # Para responses con metadata
```

**app/schemas/segmentos.py - Análisis Detallado:**
```python
class SegmentoBase(BaseModel):
    """
    Campos base compartidos entre operaciones
    - Validación automática de tipos
    - Documentación integrada con FastAPI
    - Serialización JSON automática
    """
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    longitud: float = Field(..., ge=-180, le=180)  # Validación GPS
    latitud: float = Field(..., ge=-90, le=90)     # Validación GPS
    ubicacion: Optional[str] = Field(None, max_length=100)

class SegmentoCreate(SegmentoBase):
    """Validación específica para creación"""
    pass  # Hereda todo de Base

class SegmentoResponse(SegmentoBase):
    """Response con metadata del sistema"""
    id_segmento: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Para compatibilidad con ORMs
```

**Validaciones Avanzadas Implementadas:**
- **Coordenadas GPS**: Validación de rangos geográficos válidos
- **Strings**: Longitud mínima/máxima configurada
- **Fechas**: Formato ISO automático
- **IDs**: Validación de integridad referencial
- **Enums**: Valores predefinidos para campos categóricos

#### 🔄 app/services/ - Lógica de Negocio

**Arquitectura de Servicios:**
```python
# Patrón Repository implementado
# Separación clara entre controladores y acceso a datos

class BaseService:
    """Clase base con operaciones CRUD comunes"""
    
class SegmentosService(BaseService):
    """
    Responsabilidades específicas:
    1. Validación de lógica de negocio
    2. Operaciones complejas con múltiples tablas
    3. Cálculos de índices IRI
    4. Gestión de transacciones
    5. Logging y auditoría
    """
```

**app/services/segmentos_service.py - Funcionalidades:**
```python
async def create_segmento(data: SegmentoCreate) -> SegmentoResponse:
    """
    Proceso completo de creación:
    1. Validación de coordenadas únicas
    2. Inserción en tabla principal
    3. Creación de geometría inicial
    4. Inicialización de índices
    5. Log de auditoría
    """

async def calculate_segment_quality(segment_id: int) -> Dict:
    """
    Cálculo de calidad del segmento:
    1. Agregación de muestras
    2. Cálculo de IRI promedio
    3. Detección de huecos
    4. Generación de métricas
    """
```

#### 🌐 app/api/ - Definición de Endpoints

**Estructura de API:**
```python
# Router jerárquico:
app
├── /                    # Root endpoints
├── /health             # Health checks
├── /docs               # Swagger UI
├── /redoc              # ReDoc documentation
└── /api/v1/            # API versioning
    ├── /segmentos/     # Segmentos CRUD
    ├── /muestras/      # Muestras CRUD
    └── /sensores/      # Sensores CRUD
```

**app/api/endpoints/segmentos.py - Endpoints Detallados:**
```python
@router.get("/", response_model=List[SegmentoResponse])
async def list_segmentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    ubicacion: Optional[str] = Query(None)
):
    """
    Listado con funcionalidades avanzadas:
    - Paginación configurable
    - Búsqueda por texto
    - Filtros por ubicación
    - Ordenamiento múltiple
    """

@router.post("/", response_model=SegmentoResponse, status_code=201)
async def create_segmento(segmento: SegmentoCreate):
    """
    Creación con validación completa:
    - Validación de schema automática
    - Verificación de duplicados
    - Inicialización de relaciones
    - Response con datos completos
    """

@router.get("/{segmento_id}", response_model=SegmentoResponse)
async def get_segmento(segmento_id: int = Path(..., gt=0)):
    """
    Obtención individual:
    - Validación de ID en path
    - Manejo de 404 automático
    - Carga de relaciones si es necesario
    """

@router.put("/{segmento_id}", response_model=SegmentoResponse)
async def update_segmento(
    segmento_id: int,
    segmento_update: SegmentoUpdate
):
    """
    Actualización parcial:
    - Merge de campos modificados
    - Preservación de campos no enviados
    - Validación de integridad
    - Auditoría de cambios
    """

@router.delete("/{segmento_id}", status_code=204)
async def delete_segmento(segmento_id: int):
    """
    Eliminación con integridad:
    - Verificación de dependencias
    - Soft delete opcional
    - Cascade handling
    """
```

**Funcionalidades Transversales:**
- **Error Handling**: HTTPException con códigos apropiados
- **Validación**: Automática via Pydantic
- **Documentación**: Docstrings → OpenAPI
- **Logging**: Trazabilidad completa
- **Rate Limiting**: Configuración por endpoint

---

## 🗄️ Base de Datos: Esquema y Diseño

### Modelo de Datos Conceptual

```
┌─────────────────────────────────────────────────────────────┐
│                    MODELO CONCEPTUAL RECWAY                 │
└─────────────────────────────────────────────────────────────┘

SEGMENTO (1) ←──────→ (N) GEOMETRIA
    │                     │
    │ (1)                 │
    │                     │
    ↓ (N)                 │
MUESTRA ←────────────────→ │
    │                     │
    │ (1)                 │
    │                     │
    ↓ (N)                 │
INDICES_MUESTRA           │
    │                     │
    │                     │
    ↓                     │
HUECO_MUESTRA             │
                          │
FUENTE_DATOS_DISPOSITIVO ←┘
    │ (1)
    │
    ↓ (N)
REGISTRO_SENSORES
```

### Esquema Físico Detallado

#### Tabla Central: `segmento`
```sql
CREATE TABLE segmento (
    id_segmento bigserial PRIMARY KEY,        -- PK autoincremental
    nombre varchar(50) NOT NULL,              -- Identificador humano
    tipo varchar(50),                         -- Autopista/Calle/Rural
    nodo_inicial_x double precision NOT NULL, -- GPS inicio
    nodo_final_x double precision NOT NULL,   -- GPS fin
    nodo_inicial_y double precision NOT NULL, -- GPS inicio
    nodo_final_y double precision NOT NULL,   -- GPS fin
    cantidad_muestras integer NOT NULL,       -- Counter desnormalizado
    ultima_fecha_muestra varchar(30),         -- Cache de última actividad
    longitud double precision NOT NULL,       -- Longitud calculada
    oneway boolean,                           -- Dirección única
    surface integer,                          -- Tipo de superficie
    width double precision,                   -- Ancho de vía
    error_gps double precision               -- Precisión GPS promedio
);

-- Índices de rendimiento
CREATE INDEX idx_segmento_coordinates ON segmento(nodo_inicial_x, nodo_inicial_y);
CREATE INDEX idx_segmento_tipo ON segmento(tipo);
CREATE INDEX idx_segmento_longitud ON segmento(longitud);
```

#### Geometría Detallada: `geometria`
```sql
CREATE TABLE geometria (
    id_geometria bigserial PRIMARY KEY,
    orden integer NOT NULL,                   -- Secuencia de puntos
    coordenada_x double precision NOT NULL,   -- Longitud GPS
    coordenada_y double precision NOT NULL,   -- Latitud GPS
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) 
        REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- Índices especializados
CREATE INDEX idx_geometria_segmento ON geometria(id_segmento_seleccionado);
CREATE INDEX idx_geometria_orden ON geometria(orden);
CREATE INDEX idx_geometria_coords ON geometria(coordenada_x, coordenada_y);
```

#### Datos de Sensores: `muestra`
```sql
CREATE TABLE muestra (
    id_muestra bigserial PRIMARY KEY,
    tipo_dispositivo varchar(30),             -- smartphone/sensor
    identificador_dispositivo varchar(60),    -- UUID del dispositivo
    fecha_muestra varchar(40),                -- Timestamp de recolección
    id_segmento_seleccionado integer NOT NULL,
    FOREIGN KEY (id_segmento_seleccionado) 
        REFERENCES segmento(id_segmento) ON DELETE CASCADE
);

-- Índices para consultas frecuentes
CREATE INDEX idx_muestra_segmento ON muestra(id_segmento_seleccionado);
CREATE INDEX idx_muestra_dispositivo ON muestra(identificador_dispositivo);
CREATE INDEX idx_muestra_fecha ON muestra(fecha_muestra);
```

#### Métricas de Calidad: `indices_muestra`
```sql
CREATE TABLE indices_muestra (
    id_indice_muestra bigserial PRIMARY KEY,
    nota_general double precision NOT NULL,   -- Calificación 0-10
    iri_modificado double precision NOT NULL, -- IRI adaptado
    iri_estandar double precision NOT NULL,   -- IRI internacional
    indice_primero double precision NOT NULL, -- Métrica personalizada 1
    indice_segundo double precision NOT NULL, -- Métrica personalizada 2
    iri_tercero double precision,             -- IRI adicional
    id_muestra integer NOT NULL,
    FOREIGN KEY (id_muestra) 
        REFERENCES muestra(id_muestra) ON DELETE CASCADE
);

-- Índices para análisis
CREATE INDEX idx_indices_muestra ON indices_muestra(id_muestra);
CREATE INDEX idx_indices_iri ON indices_muestra(iri_modificado);
CREATE INDEX idx_indices_nota ON indices_muestra(nota_general);
```

#### Metadatos de Dispositivos: `fuente_datos_dispositivo`
```sql
CREATE TABLE fuente_datos_dispositivo (
    id_fuente bigserial PRIMARY KEY,
    device_id varchar(100),                   -- ID único del dispositivo
    session_id varchar(100),                  -- Sesión de recolección
    platform varchar(50),                     -- Android/iOS/Other
    device_model varchar(100),                -- Modelo específico
    manufacturer varchar(100),                -- Fabricante
    brand varchar(100),                       -- Marca comercial
    os_version varchar(50),                   -- Versión del OS
    app_version varchar(100),                 -- Versión de la app
    company varchar(100),                     -- Organización
    android_id varchar(100),                  -- ID específico Android
    battery_info varchar(100),                -- Estado de batería
    acc_available boolean,                    -- Acelerómetro disponible
    acc_info varchar(100),                    -- Info del acelerómetro
    gyro_available boolean,                   -- Giroscopio disponible
    gyro_info varchar(100),                   -- Info del giroscopio
    gps_available boolean,                    -- GPS disponible
    gps_info varchar(100),                    -- Info del GPS
    export_date timestamp,                    -- Fecha de exportación
    total_records integer,                    -- Total de registros
    sampling_rate real,                       -- Frecuencia de muestreo
    recording_duration varchar(20),           -- Duración de grabación
    average_sample_rate real                  -- Frecuencia promedio
);
```

#### Datos Raw de Sensores: `registro_sensores`
```sql
CREATE TABLE registro_sensores (
    id_registro bigserial PRIMARY KEY,
    timestamp bigint NOT NULL,                -- Timestamp Unix
    acc_x double precision,                   -- Aceleración X
    acc_y double precision,                   -- Aceleración Y
    acc_z double precision,                   -- Aceleración Z
    acc_magnitude double precision,           -- Magnitud aceleración
    gyro_x double precision,                  -- Giroscopio X
    gyro_y double precision,                  -- Giroscopio Y
    gyro_z double precision,                  -- Giroscopio Z
    gyro_magnitude double precision,          -- Magnitud giroscopio
    gps_lat double precision,                 -- Latitud GPS
    gps_lng double precision,                 -- Longitud GPS
    gps_accuracy double precision,            -- Precisión GPS
    gps_speed double precision,               -- Velocidad GPS
    gps_speed_accuracy double precision,      -- Precisión velocidad
    gps_altitude double precision,            -- Altitud
    gps_altitude_accuracy double precision,   -- Precisión altitud
    gps_heading double precision,             -- Dirección
    gps_heading_accuracy double precision,    -- Precisión dirección
    gps_timestamp bigint,                     -- Timestamp GPS
    gps_provider varchar(50),                 -- Proveedor GPS
    device_orientation double precision,      -- Orientación dispositivo
    sample_rate double precision,             -- Tasa de muestreo
    gps_changed boolean DEFAULT false,        -- Cambio en GPS
    id_fuente integer NOT NULL,
    FOREIGN KEY (id_fuente) 
        REFERENCES fuente_datos_dispositivo(id_fuente) ON DELETE CASCADE
);

-- Índices optimizados para big data
CREATE INDEX idx_registro_fuente ON registro_sensores(id_fuente);
CREATE INDEX idx_registro_timestamp ON registro_sensores(timestamp);
CREATE INDEX idx_registro_gps ON registro_sensores(gps_lat, gps_lng);
CLUSTER registro_sensores USING idx_registro_timestamp;
```

### Estrategias de Optimización

#### Particionamiento (Preparado para futuro)
```sql
-- Particionamiento por fecha para tabla registro_sensores
-- Útil cuando los datos crezcan significativamente
CREATE TABLE registro_sensores_2025_01 PARTITION OF registro_sensores
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

#### Índices Especializados
```sql
-- Índice compuesto para consultas geoespaciales
CREATE INDEX idx_gps_compound ON registro_sensores(gps_lat, gps_lng, timestamp);

-- Índice parcial para datos con GPS válido
CREATE INDEX idx_valid_gps ON registro_sensores(gps_lat, gps_lng) 
    WHERE gps_lat IS NOT NULL AND gps_lng IS NOT NULL;

-- Índice funcional para búsquedas de texto
CREATE INDEX idx_segmento_search ON segmento 
    USING gin(to_tsvector('spanish', nombre || ' ' || coalesce(tipo, '')));
```
