"""Script to check all users in database"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_all_users():
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
        
        # Verificar todos los usuarios
        cursor.execute("""
            SELECT id, email, full_name, is_email_verified, email_verification_token, registered_at
            FROM users 
            ORDER BY registered_at DESC;
        """)
        
        users = cursor.fetchall()
        
        print("Todos los usuarios en la base de datos:")
        print("-" * 80)
        for user in users:
            print(f"ID: {user[0]}")
            print(f"Email: {user[1]}")
            print(f"Nombre: {user[2]}")
            print(f"Verificado: {user[3]}")
            print(f"Token: {user[4] if user[4] else 'Sin token'}")
            print(f"Registrado: {user[5]}")
            print("-" * 80)
        
        if not users:
            print("No hay usuarios en la base de datos")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_all_users()
