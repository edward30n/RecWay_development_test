import os
from pathlib import Path

# Cargar variables de entorno desde .env si existe
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # Si no está instalado python-dotenv, solo usar variables de entorno del sistema
        pass


class Settings:
    """Configuración de la aplicación"""

    def __init__(self):
        # Proyecto
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RecWay API")
        self.VERSION: str = "1.0.0"

        # API
        self.API_V1_STR: str = "/api/v1"

        # Database
        self.postgres_server: str = os.getenv("POSTGRES_SERVER", "localhost")
        self.postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
        self.postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
        self.postgres_db: str = os.getenv("POSTGRES_DB", "recway_db")
        self.postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))

        # CORS
        self.BACKEND_CORS_ORIGINS: list = [
            "http://localhost:3000",
            "http://localhost:8080",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8080",
            "http://127.0.0.1:5173",
        ]

        # App
        self.app_name: str = self.PROJECT_NAME
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    @property
    def database_url(self) -> str:
        """URL de conexión a la base de datos"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def pg_conn(self) -> str:
        """Para compatibilidad con el código anterior"""
        return os.getenv("PG_CONN", self.database_url)


settings = Settings()
