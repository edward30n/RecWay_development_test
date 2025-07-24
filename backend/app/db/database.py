import asyncpg  # type: ignore
from typing import Optional
from app.core.config import settings

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        """Crear el pool de conexiones a la base de datos"""
        self.pool = await asyncpg.create_pool(
            dsn=settings.database_url,
            min_size=1,
            max_size=10,
        )
    
    async def disconnect(self) -> None:
        """Cerrar el pool de conexiones"""
        if self.pool:
            await self.pool.close()
    
    async def get_connection(self):
        """Obtener una conexión del pool"""
        if not self.pool:
            await self.connect()
        return self.pool.acquire()

# Instancia global de la base de datos
database = Database()
