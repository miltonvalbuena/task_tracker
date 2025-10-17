#!/usr/bin/env python3
"""
Script para verificar el esquema de la base de datos en Railway
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from sqlalchemy import inspect, text

def check_railway_schema():
    """Verificar el esquema de la base de datos en Railway"""
    print("🔍 Verificando esquema de la base de datos en Railway...")
    
    db = SessionLocal()
    try:
        # Obtener información del inspector
        inspector = inspect(engine)
        
        # Listar todas las tablas
        tables = inspector.get_table_names()
        print(f"📊 Tablas en la base de datos: {tables}")
        
        # Verificar estructura de la tabla users
        if 'users' in tables:
            print("\n👥 Estructura de la tabla 'users':")
            columns = inspector.get_columns('users')
            for column in columns:
                print(f"   - {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        # Verificar estructura de la tabla clients
        if 'clients' in tables:
            print("\n🏢 Estructura de la tabla 'clients':")
            columns = inspector.get_columns('clients')
            for column in columns:
                print(f"   - {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        # Verificar estructura de la tabla tasks
        if 'tasks' in tables:
            print("\n📝 Estructura de la tabla 'tasks':")
            columns = inspector.get_columns('tasks')
            for column in columns:
                print(f"   - {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        # Verificar estructura de la tabla arls
        if 'arls' in tables:
            print("\n📋 Estructura de la tabla 'arls':")
            columns = inspector.get_columns('arls')
            for column in columns:
                print(f"   - {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        # Verificar si hay tablas con nombres diferentes
        for table in tables:
            if 'company' in table.lower():
                print(f"\n🏢 Tabla relacionada con company: {table}")
                columns = inspector.get_columns(table)
                for column in columns:
                    print(f"   - {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        print("\n✅ Verificación del esquema completada")
        
    except Exception as e:
        print(f"❌ Error verificando esquema: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_railway_schema()
