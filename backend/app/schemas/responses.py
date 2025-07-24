from typing import List, Optional

from pydantic import BaseModel

from .muestras import HuecoMuestra, IndicesMuestra, Muestra
from .segmentos import Geometria, HuecoSegmento, IndicesSegmento, Segmento
from .sensores import FuenteDatosDispositivo, RegistroSensores

# Modelo para respuestas GeoJSON


class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: List[List[float]]


class GeoJSONProperties(BaseModel):
    id_segmento: int
    nombre: str
    tipo: Optional[str] = None
    cantidad_muestras: int
    ultima_fecha_muestra: Optional[str] = None
    longitud: float
    # Datos de índices si están disponibles
    nota_general: Optional[float] = None
    iri_modificado: Optional[float] = None
    iri_estandar: Optional[float] = None


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: GeoJSONProperties


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]


# Modelo para respuesta completa de segmento con todos sus datos relacionados


class SegmentoCompleto(BaseModel):
    segmento: Segmento
    geometrias: List[Geometria]
    indices: Optional[IndicesSegmento] = None
    huecos: List[HuecoSegmento]
    muestras: List[Muestra]


# Modelo para respuesta completa de muestra con todos sus datos relacionados


class MuestraCompleta(BaseModel):
    muestra: Muestra
    indices: Optional[IndicesMuestra] = None
    huecos: List[HuecoMuestra]


# Modelo para respuesta completa de datos de sensores


class DatosSensoresCompletos(BaseModel):
    fuente: FuenteDatosDispositivo
    registros: List[RegistroSensores]


# Modelo de respuesta estándar para operaciones


class RespuestaOperacion(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
