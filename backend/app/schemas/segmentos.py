from typing import Optional

from pydantic import BaseModel


# Modelos para Segmento (con nuevos campos)
class SegmentoBase(BaseModel):
    nombre: str
    tipo: Optional[str] = None
    nodo_inicial_x: float
    nodo_final_x: float
    nodo_inicial_y: float
    nodo_final_y: float
    cantidad_muestras: int
    ultima_fecha_muestra: Optional[str] = None
    longitud: float
    oneway: Optional[bool] = None
    surface: Optional[int] = None
    width: Optional[float] = None
    error_gps: Optional[float] = None


class SegmentoCreate(SegmentoBase):
    pass


class Segmento(SegmentoBase):
    id_segmento: int

    class Config:
        from_attributes = True


# Modelos para Geometría (campos actualizados)
class GeometriaBase(BaseModel):
    orden: int
    coordenada_x: float
    coordenada_y: float
    id_segmento_seleccionado: int


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
    id_segmento_seleccionado: int


class IndicesSegmentoCreate(IndicesSegmentoBase):
    pass


class IndicesSegmento(IndicesSegmentoBase):
    id_indice_segmento: int

    class Config:
        from_attributes = True


# Modelos para Huecos de Segmento (con nuevos campos)
class HuecoSegmentoBase(BaseModel):
    latitud: float
    longitud: float
    magnitud: float
    velocidad: float
    ultima_fecha_muestra: Optional[str] = None
    error_gps: Optional[float] = None
    id_segmento_seleccionado: int


class HuecoSegmentoCreate(HuecoSegmentoBase):
    pass


class HuecoSegmento(HuecoSegmentoBase):
    id_hueco_segmento: int

    class Config:
        from_attributes = True
