from typing import List, Optional

from app.db.database import database
from app.schemas.muestras import Muestra, MuestraCreate
from app.schemas.responses import MuestraCompleta


class MuestraService:
    """Servicio para manejar operaciones de muestras"""

    async def get_all_muestras(self) -> List[Muestra]:
        """Obtener todas las muestras"""
        async with database.get_connection() as conn:
            rows = await conn.fetch("SELECT * FROM muestra ORDER BY id_muestra")
            return [Muestra(**dict(row)) for row in rows]

    async def get_muestra_by_id(self, id_muestra: int) -> Optional[Muestra]:
        """Obtener una muestra por ID"""
        async with database.get_connection() as conn:
            row = await conn.fetchrow("SELECT * FROM muestra WHERE id_muestra = $1", id_muestra)
            return Muestra(**dict(row)) if row else None

    async def get_muestras_by_segmento(self, id_segmento: int) -> List[Muestra]:
        """Obtener todas las muestras de un segmento"""
        async with database.get_connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM muestra WHERE id_segmento_seleccionado = $1 ORDER BY id_muestra", id_segmento
            )
            return [Muestra(**dict(row)) for row in rows]

    async def create_muestra(self, muestra: MuestraCreate) -> Muestra:
        """Crear una nueva muestra"""
        async with database.get_connection() as conn:
            query = """
            INSERT INTO muestra (tipo_dispositivo, identificador_dispositivo, fecha_muestra, id_segmento_seleccionado)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """
            row = await conn.fetchrow(
                query,
                muestra.tipo_dispositivo,
                muestra.identificador_dispositivo,
                muestra.fecha_muestra,
                muestra.id_segmento_seleccionado,
            )
            return Muestra(**dict(row))

    async def get_indices_by_muestra(self, id_muestra: int):
        """Obtener los índices de una muestra (tabla actualizada)"""
        async with database.get_connection() as conn:
            row = await conn.fetchrow("SELECT * FROM indices_muestra WHERE id_muestra = $1", id_muestra)
            return dict(row) if row else None

    async def get_huecos_by_muestra(self, id_muestra: int):
        """Obtener los huecos de una muestra"""
        async with database.get_connection() as conn:
            rows = await conn.fetch("SELECT * FROM huecoMuestra WHERE id_muestra_seleccionada = $1", id_muestra)
            return [dict(row) for row in rows]

    async def get_muestra_completa(self, id_muestra: int) -> Optional[MuestraCompleta]:
        """Obtener una muestra con todos sus datos relacionados"""
        muestra = await self.get_muestra_by_id(id_muestra)
        if not muestra:
            return None

        indices = await self.get_indices_by_muestra(id_muestra)
        huecos = await self.get_huecos_by_muestra(id_muestra)

        return MuestraCompleta(muestra=muestra, indices=indices, huecos=huecos)


# Instancia del servicio
muestra_service = MuestraService()
