#!/usr/bin/env python3
"""
Script para crear la tabla countries y poblarla con datos
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def create_countries_table():
    """Crear tabla countries y poblarla"""
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect('postgresql://postgres:edward123@localhost:5432/recWay_db')
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print('🔗 Conectado a la base de datos')
        
        # Crear tabla countries si no existe
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            code VARCHAR(2) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            phone_prefix VARCHAR(10) NOT NULL
        );
        """
        
        cursor.execute(create_table_sql)
        print('✅ Tabla countries creada/verificada')
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) as count FROM countries")
        count = cursor.fetchone()['count']
        
        if count == 0:
            print('📝 Insertando países...')
            
            # Datos de países
            countries_data = [
                ('AR', 'Argentina', '+54'),
                ('BR', 'Brazil', '+55'),
                ('CA', 'Canada', '+1'),
                ('CL', 'Chile', '+56'),
                ('CO', 'Colombia', '+57'),
                ('EC', 'Ecuador', '+593'),
                ('ES', 'Spain', '+34'),
                ('FR', 'France', '+33'),
                ('DE', 'Germany', '+49'),
                ('IT', 'Italy', '+39'),
                ('MX', 'Mexico', '+52'),
                ('PE', 'Peru', '+51'),
                ('GB', 'United Kingdom', '+44'),
                ('US', 'United States', '+1'),
                ('VE', 'Venezuela', '+58'),
            ]
            
            # Insertar países
            insert_sql = """
            INSERT INTO countries (code, name, phone_prefix) 
            VALUES (%s, %s, %s)
            ON CONFLICT (code) DO NOTHING
            """
            
            cursor.executemany(insert_sql, countries_data)
            print(f'✅ {len(countries_data)} países insertados')
        else:
            print(f'📊 Ya existen {count} países en la BD')
        
        # Confirmar cambios
        conn.commit()
        
        # Mostrar países insertados
        cursor.execute("SELECT code, name, phone_prefix FROM countries ORDER BY name")
        countries = cursor.fetchall()
        
        print(f'\n📋 Países disponibles ({len(countries)}):')
        for country in countries:
            print(f"  {country['code']}: {country['name']} ({country['phone_prefix']})")
        
        cursor.close()
        conn.close()
        print('\n✅ Proceso completado exitosamente')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    create_countries_table()
