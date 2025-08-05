from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URI = os.getenv("DATABASE_URI")

def run_migration():
    # Crear el engine de SQLAlchemy
    engine = create_engine(DATABASE_URI)
    
    # Ejecutar la migración
    with engine.connect() as connection:
        try:
            # Añadir la columna email_verified_at
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMP WITH TIME ZONE;
            """))
            connection.commit()
            print("Migración completada exitosamente")
        except Exception as e:
            print(f"Error durante la migración: {e}")
            connection.rollback()

if __name__ == "__main__":
    run_migration()
