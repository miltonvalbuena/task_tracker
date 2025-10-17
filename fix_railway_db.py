#!/usr/bin/env python3
"""
Script para corregir la base de datos en Railway
Se ejecuta localmente pero se conecta a la base de datos de Railway
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def get_railway_db_url():
    """Obtener la URL de la base de datos de Railway"""
    # Esta URL debe ser reemplazada por la URL real de Railway
    # Se puede obtener con: railway variables | grep DATABASE_URL
    return "postgresql://postgres:BzRxVJCPTMGrxSPhOXJcTvXFZAdvrnYE@postgres-c92c.railway.internal:5432/railway"

def fix_database():
    """Corregir la estructura de la base de datos"""
    print("🔧 Conectando a la base de datos de Railway...")
    
    try:
        # Parsear la URL de la base de datos
        url = get_railway_db_url()
        parsed = urlparse(url)
        
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
        
        # Verificar si la columna client_id existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'client_id'
        """)
        
        if not cursor.fetchone():
            print("🔧 Agregando columna client_id a la tabla users...")
            
            # Agregar la columna client_id
            cursor.execute("ALTER TABLE users ADD COLUMN client_id INTEGER")
            
            # Agregar la foreign key constraint
            cursor.execute("""
                ALTER TABLE users 
                ADD CONSTRAINT fk_users_client_id 
                FOREIGN KEY (client_id) REFERENCES clients(id)
            """)
            
            conn.commit()
            print("✅ Columna client_id agregada exitosamente")
        else:
            print("✅ Columna client_id ya existe")
        
        # Verificar si existe la tabla clients
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'clients'
        """)
        
        if not cursor.fetchone():
            print("🔧 Creando tabla clients...")
            
            # Crear tabla clients
            cursor.execute("""
                CREATE TABLE clients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    custom_fields_config JSONB DEFAULT '[]',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)
            
            conn.commit()
            print("✅ Tabla clients creada exitosamente")
        else:
            print("✅ Tabla clients ya existe")
        
        # Verificar si existe la tabla arls
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'arls'
        """)
        
        if not cursor.fetchone():
            print("🔧 Creando tabla arls...")
            
            # Crear tabla arls
            cursor.execute("""
                CREATE TABLE arls (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)
            
            conn.commit()
            print("✅ Tabla arls creada exitosamente")
        else:
            print("✅ Tabla arls ya existe")
        
        # Crear un cliente por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]
        
        if client_count == 0:
            print("🔧 Creando cliente por defecto...")
            cursor.execute("""
                INSERT INTO clients (name, description, is_active, custom_fields_config)
                VALUES ('EMPRESA PRINCIPAL', 'Empresa principal del sistema', TRUE, '[]')
            """)
            conn.commit()
            print("✅ Cliente por defecto creado")
        else:
            print("✅ Clientes ya existen")
        
        cursor.close()
        conn.close()
        
        print("✅ Base de datos corregida exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo la base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Corrigiendo base de datos de Railway...")
    if fix_database():
        print("🎉 ¡Base de datos corregida exitosamente!")
    else:
        print("❌ Error corrigiendo la base de datos")
        sys.exit(1)
