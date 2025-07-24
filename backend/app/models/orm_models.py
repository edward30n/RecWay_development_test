"""
Modelos ORM opcionales para RecWay usando SQLAlchemy
Estos NO son necesarios con nuestro enfoque actual, pero pueden ser útiles
para casos específicos donde queramos usar ORM en lugar de SQL raw.
"""

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Float,
                        ForeignKey, Integer, String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Segmento(Base):
    """Modelo ORM para la tabla segmento"""

    __tablename__ = "segmento"

    id_segmento = Column(BigInteger, primary_key=True)
    nombre = Column(String(50), nullable=False)
    tipo = Column(String(50))
    nodo_inicial_x = Column(Float, nullable=False)
    nodo_final_x = Column(Float, nullable=False)
    nodo_inicial_y = Column(Float, nullable=False)
    nodo_final_y = Column(Float, nullable=False)
    cantidad_muestras = Column(Integer, nullable=False)
    ultima_fecha_muestra = Column(String(30))
    longitud = Column(Float, nullable=False)
    oneway = Column(Boolean)
    surface = Column(Integer)
    width = Column(Float)
    error_gps = Column(Float)

    # Relaciones
    geometrias = relationship(
        "Geometria", back_populates="segmento", cascade="all, delete-orphan"
    )
    indices = relationship(
        "IndicesSegmento", back_populates="segmento", cascade="all, delete-orphan"
    )
    huecos = relationship(
        "HuecoSegmento", back_populates="segmento", cascade="all, delete-orphan"
    )
    muestras = relationship(
        "Muestra", back_populates="segmento", cascade="all, delete-orphan"
    )


class Geometria(Base):
    """Modelo ORM para la tabla geometria"""

    __tablename__ = "geometria"

    id_geometria = Column(BigInteger, primary_key=True)
    orden = Column(Integer, nullable=False)
    coordenada_x = Column(Float, nullable=False)
    coordenada_y = Column(Float, nullable=False)
    id_segmento_seleccionado = Column(Integer, ForeignKey("segmento.id_segmento"))

    # Relación
    segmento = relationship("Segmento", back_populates="geometrias")


class IndicesSegmento(Base):
    """Modelo ORM para la tabla indicesSegmento"""

    __tablename__ = "indicesSegmento"

    id_indice_segmento = Column(BigInteger, primary_key=True)
    nota_general = Column(Float, nullable=False)
    iri_modificado = Column(Float, nullable=False)
    iri_estandar = Column(Float, nullable=False)
    indice_primero = Column(Float, nullable=False)
    indice_segundo = Column(Float, nullable=False)
    iri_tercero = Column(Float)
    id_segmento_seleccionado = Column(Integer, ForeignKey("segmento.id_segmento"))

    # Relación
    segmento = relationship("Segmento", back_populates="indices")


class HuecoSegmento(Base):
    """Modelo ORM para la tabla huecoSegmento"""

    __tablename__ = "huecoSegmento"

    id_hueco_segmento = Column(BigInteger, primary_key=True)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    magnitud = Column(Float, nullable=False)
    velocidad = Column(Float, nullable=False)
    ultima_fecha_muestra = Column(String(30))
    error_gps = Column(Float)
    id_segmento_seleccionado = Column(Integer, ForeignKey("segmento.id_segmento"))

    # Relación
    segmento = relationship("Segmento", back_populates="huecos")


class Muestra(Base):
    """Modelo ORM para la tabla muestra"""

    __tablename__ = "muestra"

    id_muestra = Column(BigInteger, primary_key=True)
    tipo_dispositivo = Column(String(30))
    identificador_dispositivo = Column(String(60))
    fecha_muestra = Column(String(40))
    id_segmento_seleccionado = Column(Integer, ForeignKey("segmento.id_segmento"))

    # Relaciones
    segmento = relationship("Segmento", back_populates="muestras")
    indices = relationship(
        "IndicesMuestra", back_populates="muestra", cascade="all, delete-orphan"
    )
    huecos = relationship(
        "HuecoMuestra", back_populates="muestra", cascade="all, delete-orphan"
    )


class IndicesMuestra(Base):
    """Modelo ORM para la tabla indices_muestra"""

    __tablename__ = "indices_muestra"

    id_indice_muestra = Column(BigInteger, primary_key=True)
    nota_general = Column(Float, nullable=False)
    iri_modificado = Column(Float, nullable=False)
    iri_estandar = Column(Float, nullable=False)
    indice_primero = Column(Float, nullable=False)
    indice_segundo = Column(Float, nullable=False)
    iri_tercero = Column(Float)
    id_muestra = Column(Integer, ForeignKey("muestra.id_muestra"))

    # Relación
    muestra = relationship("Muestra", back_populates="indices")


class HuecoMuestra(Base):
    """Modelo ORM para la tabla huecoMuestra"""

    __tablename__ = "huecoMuestra"

    id_hueco_muestra = Column(BigInteger, primary_key=True)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    magnitud = Column(Float, nullable=False)
    velocidad = Column(Float, nullable=False)
    id_muestra_seleccionada = Column(Integer, ForeignKey("muestra.id_muestra"))

    # Relación
    muestra = relationship("Muestra", back_populates="huecos")


class FuenteDatosDispositivo(Base):
    """Modelo ORM para la tabla fuente_datos_dispositivo"""

    __tablename__ = "fuente_datos_dispositivo"

    id_fuente = Column(BigInteger, primary_key=True)
    device_id = Column(String(100))
    session_id = Column(String(100))
    platform = Column(String(50))
    device_model = Column(String(100))
    manufacturer = Column(String(100))
    brand = Column(String(100))
    os_version = Column(String(50))
    app_version = Column(String(100))
    company = Column(String(100))
    android_id = Column(String(100))
    battery_info = Column(String(100))
    acc_available = Column(Boolean)
    acc_info = Column(String(100))
    gyro_available = Column(Boolean)
    gyro_info = Column(String(100))
    gps_available = Column(Boolean)
    gps_info = Column(String(100))
    export_date = Column(DateTime)
    total_records = Column(Integer)
    sampling_rate = Column(Float)
    recording_duration = Column(String(20))
    average_sample_rate = Column(Float)

    # Relaciones
    registros = relationship(
        "RegistroSensores", back_populates="fuente", cascade="all, delete-orphan"
    )


class RegistroSensores(Base):
    """Modelo ORM para la tabla registro_sensores"""

    __tablename__ = "registro_sensores"

    id_registro = Column(BigInteger, primary_key=True)
    timestamp = Column(BigInteger, nullable=False)
    acc_x = Column(Float)
    acc_y = Column(Float)
    acc_z = Column(Float)
    acc_magnitude = Column(Float)
    gyro_x = Column(Float)
    gyro_y = Column(Float)
    gyro_z = Column(Float)
    gyro_magnitude = Column(Float)
    gps_lat = Column(Float)
    gps_lng = Column(Float)
    gps_accuracy = Column(Float)
    gps_speed = Column(Float)
    gps_speed_accuracy = Column(Float)
    gps_altitude = Column(Float)
    gps_altitude_accuracy = Column(Float)
    gps_heading = Column(Float)
    gps_heading_accuracy = Column(Float)
    gps_timestamp = Column(BigInteger)
    gps_provider = Column(String(50))
    device_orientation = Column(Float)
    sample_rate = Column(Float)
    gps_changed = Column(Boolean, default=False)
    id_fuente = Column(Integer, ForeignKey("fuente_datos_dispositivo.id_fuente"))

    # Relación
    fuente = relationship("FuenteDatosDispositivo", back_populates="registros")


# NOTA IMPORTANTE:
# Estos modelos ORM SON OPCIONALES y NO se están usando actualmente.
# Nuestro enfoque actual usa SQL raw + Pydantic schemas, que es más eficiente
# para las consultas GeoJSON complejas que necesita RecWay.
#
# Si quisieras usar estos modelos ORM, necesitarías:
# 1. pip install sqlalchemy
# 2. Configurar una session de SQLAlchemy en lugar de asyncpg
# 3. Reescribir los servicios para usar ORM en lugar de SQL raw
