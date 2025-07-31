#!/usr/bin/env python3
"""
Script para agregar países a la base de datos
"""

from app.db.database import SessionLocal
from app.models.user import Country

def add_countries():
    """Add countries to database"""
    db = SessionLocal()
    try:
        # Lista de países para agregar
        countries_to_add = [
            ('CO', 'Colombia', '+57'),
            ('US', 'United States', '+1'),
            ('MX', 'Mexico', '+52'),
            ('AR', 'Argentina', '+54'),
            ('BR', 'Brazil', '+55'),
            ('PE', 'Peru', '+51'),
            ('EC', 'Ecuador', '+593'),
            ('VE', 'Venezuela', '+58'),
            ('CL', 'Chile', '+56'),
            ('UY', 'Uruguay', '+598'),
            ('PY', 'Paraguay', '+595'),
            ('BO', 'Bolivia', '+591'),
            ('PA', 'Panama', '+507'),
            ('CR', 'Costa Rica', '+506'),
            ('GT', 'Guatemala', '+502'),
            ('HN', 'Honduras', '+504'),
            ('SV', 'El Salvador', '+503'),
            ('NI', 'Nicaragua', '+505'),
            ('ES', 'Spain', '+34'),
        ]
        
        added_count = 0
        for code, name, prefix in countries_to_add:
            # Verificar si ya existe
            exists = db.query(Country).filter(Country.code == code).first()
            if not exists:
                country = Country(code=code, name=name, phone_prefix=prefix)
                db.add(country)
                added_count += 1
                print(f"Agregado: {code} - {name} ({prefix})")
            else:
                print(f"Ya existe: {code} - {name}")
        
        db.commit()
        print(f"\n✅ Proceso completado. Se agregaron {added_count} países.")
        
        # Mostrar todos los países en la BD
        all_countries = db.query(Country).order_by(Country.code).all()
        print(f"\n📊 Total países en BD: {len(all_countries)}")
        print("\nPaíses disponibles:")
        for country in all_countries:
            print(f"  {country.code}: {country.name} ({country.phone_prefix})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_countries()
