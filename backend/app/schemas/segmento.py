from typing import Optional

from pydantic import BaseModel

# Modelos para Segmento


class SegmentoBase(BaseModel):
    nombre: str
    tipo: Optional[str] = None
    latitud_origen: float
    latitud_destino: float
    longitud_origen: float
    longitud_destino: float
    cantidad_muestras: int
    ultima_fecha_muestra: Optional[str] = None
    longitud: float


class SegmentoCreate(SegmentoBase):
    pass


class Segmento(SegmentoBase):
    id_segmento: float

    class Config:
        from_attributes = True

# Modelos para Geometría


class GeometriaBase(BaseModel):
    orden: int
    longitud: float
    latitud: float
    id_segmento_seleccionado: float


class GeometriaCreate(GeometriaBase):
    pass


class Geometria(GeometriaBase):
    id_geometria: int

    class Config:
        from_attributes = True

# Modelos para Índices de Segmento


class IndicesSegmentoBase(BaseModel):
    nota_general: float
    iri_modificado: float
    iri_estandar: float
    indice_primero: float
    indice_segundo: float
    iri_tercero: Optional[float] = None
    id_segmento_seleccionado: float


class IndicesSegmentoCreate(IndicesSegmentoBase):
    pass


class IndicesSegmento(IndicesSegmentoBase):
    id_indice_segmento: int

    class Config:
        from_attributes = True

# Modelos para Huecos de Segmento


class HuecoSegmentoBase(BaseModel):
    latitud: float
    longitud: float
    magnitud: float
    velocidad: float
    ultima_fecha_muestra: Optional[str] = None
    id_segmento_seleccionado: float


class HuecoSegmentoCreate(HuecoSegmentoBase):
    pass


class HuecoSegmento(HuecoSegmentoBase):
    id_hueco_segmento: int

    class Config:
        from_attributes = True
