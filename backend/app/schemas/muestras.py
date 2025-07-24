from typing import Optional

from pydantic import BaseModel


# Modelos para Muestra
class MuestraBase(BaseModel):
    tipo_dispositivo: Optional[str] = None
    identificador_dispositivo: Optional[str] = None
    fecha_muestra: Optional[str] = None
    id_segmento_seleccionado: int


class MuestraCreate(MuestraBase):
    pass


class Muestra(MuestraBase):
    id_muestra: int

    class Config:
        from_attributes = True


# Modelos para Índices de Muestra (tabla actualizada)
class IndicesMuestraBase(BaseModel):
    nota_general: float
    iri_modificado: float
    iri_estandar: float
    indice_primero: float
    indice_segundo: float
    iri_tercero: Optional[float] = None
    id_muestra: int  # Cambió el nombre del campo


class IndicesMuestraCreate(IndicesMuestraBase):
    pass


class IndicesMuestra(IndicesMuestraBase):
    id_indice_muestra: int

    class Config:
        from_attributes = True


# Modelos para Huecos de Muestra
class HuecoMuestraBase(BaseModel):
    latitud: float
    longitud: float
    magnitud: float
    velocidad: float
    id_muestra_seleccionada: int


class HuecoMuestraCreate(HuecoMuestraBase):
    pass


class HuecoMuestra(HuecoMuestraBase):
    id_hueco_muestra: int

    class Config:
        from_attributes = True
