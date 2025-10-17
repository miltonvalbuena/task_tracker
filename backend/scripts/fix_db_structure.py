#!/usr/bin/env python3
"""
Script para corregir la estructura de la base de datos
Se ejecuta automáticamente al iniciar la aplicación
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def fix_database_structure():
    """Corregir la estructura de la base de datos"""
    print("🔧 Corrigiendo estructura de la base de datos...")
    
    try:
        # Obtener la URL de la base de datos desde las variables de entorno
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL no está configurada")
            return False
        
        # Parsear la URL de la base de datos
        parsed = urlparse(database_url)
        
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remover el '/' inicial
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        print("✅ Conectado a la base de datos")
        
        # Verificar si la columna client_id existe en users
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'client_id'
        """)
        
        if not cursor.fetchone():
            print("🔧 Agregando columna client_id a la tabla users...")
            
            # Agregar la columna client_id
            cursor.execute("ALTER TABLE users ADD COLUMN client_id INTEGER")
            
            # Agregar la foreign key constraint si la tabla clients existe
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'clients'
            """)
            
            if cursor.fetchone():
                cursor.execute("""
                    ALTER TABLE users 
                    ADD CONSTRAINT fk_users_client_id 
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                """)
            
            conn.commit()
            print("✅ Columna client_id agregada exitosamente")
        else:
            print("✅ Columna client_id ya existe")
        
        cursor.close()
        conn.close()
        
        print("✅ Estructura de base de datos corregida")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo estructura de base de datos: {e}")
        return False

if __name__ == "__main__":
    fix_database_structure()
