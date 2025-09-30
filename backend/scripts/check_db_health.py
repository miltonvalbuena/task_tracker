#!/usr/bin/env python3
"""
Script para verificar la salud de la conexión a la base de datos
"""

import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_database_connection():
    """Verificar la conexión a la base de datos"""
    print("🔍 Verificando conexión a la base de datos...")
    
    # Obtener la URL de la base de datos
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL no encontrada en variables de entorno")
        return False
    
    print(f"📊 URL de base de datos: {database_url[:50]}...")
    
    try:
        # Crear engine
        engine = create_engine(database_url, pool_pre_ping=True)
        
        # Intentar conectar
        with engine.connect() as conn:
            # Ejecutar una consulta simple
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Conexión a base de datos exitosa")
                
                # Verificar información de la base de datos
                try:
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"📊 Versión de PostgreSQL: {version}")
                except Exception as e:
                    print(f"⚠️ No se pudo obtener la versión: {e}")
                
                return True
            else:
                print("❌ Consulta de prueba falló")
                return False
                
    except OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def check_database_tables():
    """Verificar que las tablas existan"""
    print("🔍 Verificando tablas de la base de datos...")
    
    try:
        from app.database import engine
        from app.models import Base
        
        # Verificar que las tablas existan
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'companies', 'tasks']
        missing_tables = []
        
        for table in expected_tables:
            if table in tables:
                print(f"✅ Tabla '{table}' existe")
            else:
                print(f"❌ Tabla '{table}' no existe")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"⚠️ Tablas faltantes: {missing_tables}")
            return False
        else:
            print("✅ Todas las tablas necesarias existen")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def wait_for_database(max_attempts=30, delay=5):
    """Esperar a que la base de datos esté disponible"""
    print(f"⏳ Esperando a que la base de datos esté disponible (máximo {max_attempts * delay} segundos)...")
    
    for attempt in range(max_attempts):
        if check_database_connection():
            return True
        
        if attempt < max_attempts - 1:
            print(f"Intento {attempt + 1}/{max_attempts}: Esperando {delay} segundos...")
            time.sleep(delay)
    
    print(f"❌ No se pudo conectar a la base de datos después de {max_attempts} intentos")
    return False

def main():
    """Función principal"""
    print("🚀 Verificando salud de la base de datos...")
    print("=" * 50)
    
    # Verificar variables de entorno
    print("🔍 Verificando variables de entorno...")
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print("✅ DATABASE_URL configurada")
    else:
        print("❌ DATABASE_URL no configurada")
        return False
    
    print("=" * 50)
    
    # Esperar a que la base de datos esté disponible
    if not wait_for_database():
        return False
    
    print("=" * 50)
    
    # Verificar tablas
    if not check_database_tables():
        print("⚠️ Algunas tablas no existen, pero la conexión funciona")
    
    print("=" * 50)
    print("✅ Verificación de salud completada")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
