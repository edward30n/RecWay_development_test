"""Script to check database table structure"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_table_structure():
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
        
        # Verificar estructura de la tabla users
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("Estructura de la tabla 'users':")
        print("-" * 50)
        for column in columns:
            print(f"{column[0]:30} {column[1]:20} {column[2]}")
        
        # Verificar si existe email_verified_at específicamente
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'email_verified_at';
        """)
        
        result = cursor.fetchone()
        
        if result:
            print(f"\n✅ La columna 'email_verified_at' EXISTE en la tabla users")
        else:
            print(f"\n❌ La columna 'email_verified_at' NO EXISTE en la tabla users")
            
            # Intentar crear la columna manualmente
            print("\nIntentando crear la columna manualmente...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMP WITH TIME ZONE;
            """)
            conn.commit()
            print("✅ Columna creada exitosamente")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_table_structure()
