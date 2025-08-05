"""Script to remove email_verified_at column"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def remove_column():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", 5432),
            database=os.getenv("POSTGRES_DB", "recWay_db"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "edward123")
        )
        
        cursor = conn.cursor()
        
        # Verificar si la columna existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'email_verified_at';
        """)
        
        result = cursor.fetchone()
        
        if result:
            print("Eliminando la columna email_verified_at...")
            cursor.execute("ALTER TABLE users DROP COLUMN email_verified_at;")
            conn.commit()
            print("✅ Columna eliminada exitosamente")
        else:
            print("ℹ️ La columna email_verified_at no existe")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    remove_column()
