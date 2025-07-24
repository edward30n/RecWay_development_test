from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Modelos para Fuente de Datos del Dispositivo
class FuenteDatosDispositivoBase(BaseModel):
    device_id: Optional[str] = None
    session_id: Optional[str] = None
    platform: Optional[str] = None
    device_model: Optional[str] = None
    manufacturer: Optional[str] = None
    brand: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
    company: Optional[str] = None
    android_id: Optional[str] = None
    battery_info: Optional[str] = None
    acc_available: Optional[bool] = None
    acc_info: Optional[str] = None
    gyro_available: Optional[bool] = None
    gyro_info: Optional[str] = None
    gps_available: Optional[bool] = None
    gps_info: Optional[str] = None
    export_date: Optional[datetime] = None
    total_records: Optional[int] = None
    sampling_rate: Optional[float] = None
    recording_duration: Optional[str] = None
    average_sample_rate: Optional[float] = None


class FuenteDatosDispositivoCreate(FuenteDatosDispositivoBase):
    pass


class FuenteDatosDispositivo(FuenteDatosDispositivoBase):
    id_fuente: int

    class Config:
        from_attributes = True


# Modelos para Registro de Sensores
class RegistroSensoresBase(BaseModel):
    timestamp: int
    acc_x: Optional[float] = None
    acc_y: Optional[float] = None
    acc_z: Optional[float] = None
    acc_magnitude: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None
    gyro_magnitude: Optional[float] = None
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    gps_accuracy: Optional[float] = None
    gps_speed: Optional[float] = None
    gps_speed_accuracy: Optional[float] = None
    gps_altitude: Optional[float] = None
    gps_altitude_accuracy: Optional[float] = None
    gps_heading: Optional[float] = None
    gps_heading_accuracy: Optional[float] = None
    gps_timestamp: Optional[int] = None
    gps_provider: Optional[str] = None
    device_orientation: Optional[float] = None
    sample_rate: Optional[float] = None
    gps_changed: Optional[bool] = False
    id_fuente: int


class RegistroSensoresCreate(RegistroSensoresBase):
    pass


class RegistroSensores(RegistroSensoresBase):
    id_registro: int

    class Config:
        from_attributes = True
