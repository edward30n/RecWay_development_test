from typing import List, Optional

from app.db.database import database
from app.schemas.responses import DatosSensoresCompletos
from app.schemas.sensores import FuenteDatosDispositivo, FuenteDatosDispositivoCreate, RegistroSensores, RegistroSensoresCreate


class SensoresService:
    """Servicio para manejar operaciones de sensores y dispositivos"""

    async def get_all_fuentes(self) -> List[FuenteDatosDispositivo]:
        """Obtener todas las fuentes de datos de dispositivos"""
        async with database.get_connection() as conn:
            rows = await conn.fetch("SELECT * FROM fuente_datos_dispositivo ORDER BY id_fuente")
            return [FuenteDatosDispositivo(**dict(row)) for row in rows]

    async def get_fuente_by_id(self, id_fuente: int) -> Optional[FuenteDatosDispositivo]:
        """Obtener una fuente de datos por ID"""
        async with database.get_connection() as conn:
            row = await conn.fetchrow("SELECT * FROM fuente_datos_dispositivo WHERE id_fuente = $1", id_fuente)
            return FuenteDatosDispositivo(**dict(row)) if row else None

    async def create_fuente(self, fuente: FuenteDatosDispositivoCreate) -> FuenteDatosDispositivo:
        """Crear una nueva fuente de datos de dispositivo"""
        async with database.get_connection() as conn:
            query = """
            INSERT INTO fuente_datos_dispositivo (
                device_id, session_id, platform, device_model, manufacturer, brand,
                os_version, app_version, company, android_id, battery_info,
                acc_available, acc_info, gyro_available, gyro_info, gps_available,
                gps_info, export_date, total_records, sampling_rate, recording_duration,
                average_sample_rate
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22)
            RETURNING *
            """
            row = await conn.fetchrow(
                query,
                fuente.device_id,
                fuente.session_id,
                fuente.platform,
                fuente.device_model,
                fuente.manufacturer,
                fuente.brand,
                fuente.os_version,
                fuente.app_version,
                fuente.company,
                fuente.android_id,
                fuente.battery_info,
                fuente.acc_available,
                fuente.acc_info,
                fuente.gyro_available,
                fuente.gyro_info,
                fuente.gps_available,
                fuente.gps_info,
                fuente.export_date,
                fuente.total_records,
                fuente.sampling_rate,
                fuente.recording_duration,
                fuente.average_sample_rate,
            )
            return FuenteDatosDispositivo(**dict(row))

    async def get_registros_by_fuente(self, id_fuente: int, limit: int = 1000) -> List[RegistroSensores]:
        """Obtener registros de sensores por fuente de datos"""
        async with database.get_connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM registro_sensores WHERE id_fuente = $1 ORDER BY timestamp LIMIT $2",
                id_fuente,
                limit,
            )
            return [RegistroSensores(**dict(row)) for row in rows]

    async def create_registro(self, registro: RegistroSensoresCreate) -> RegistroSensores:
        """Crear un nuevo registro de sensores"""
        async with database.get_connection() as conn:
            query = """
            INSERT INTO registro_sensores (
                timestamp, acc_x, acc_y, acc_z, acc_magnitude, gyro_x, gyro_y, gyro_z,
                gyro_magnitude, gps_lat, gps_lng, gps_accuracy, gps_speed, gps_speed_accuracy,
                gps_altitude, gps_altitude_accuracy, gps_heading, gps_heading_accuracy,
                gps_timestamp, gps_provider, device_orientation, sample_rate, gps_changed, id_fuente
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24)
            RETURNING *
            """
            row = await conn.fetchrow(
                query,
                registro.timestamp,
                registro.acc_x,
                registro.acc_y,
                registro.acc_z,
                registro.acc_magnitude,
                registro.gyro_x,
                registro.gyro_y,
                registro.gyro_z,
                registro.gyro_magnitude,
                registro.gps_lat,
                registro.gps_lng,
                registro.gps_accuracy,
                registro.gps_speed,
                registro.gps_speed_accuracy,
                registro.gps_altitude,
                registro.gps_altitude_accuracy,
                registro.gps_heading,
                registro.gps_heading_accuracy,
                registro.gps_timestamp,
                registro.gps_provider,
                registro.device_orientation,
                registro.sample_rate,
                registro.gps_changed,
                registro.id_fuente,
            )
            return RegistroSensores(**dict(row))

    async def get_datos_completos(self, id_fuente: int) -> Optional[DatosSensoresCompletos]:
        """Obtener datos completos de una fuente con sus registros"""
        fuente = await self.get_fuente_by_id(id_fuente)
        if not fuente:
            return None

        registros = await self.get_registros_by_fuente(id_fuente)

        return DatosSensoresCompletos(fuente=fuente, registros=registros)


# Instancia del servicio
sensores_service = SensoresService()
