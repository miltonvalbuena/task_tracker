#!/usr/bin/env python3
"""
Script para actualizar la base de datos en Railway
Crea las tablas y migra la estructura de datos
"""

import os
import sys
import asyncio
import bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, User, Client, Task, ARL
from app.database import get_db, engine

def update_database_structure():
    """Actualizar la estructura de la base de datos"""
    print("🔧 Actualizando estructura de la base de datos...")
    
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas/actualizadas exitosamente")
        
        # Verificar si la columna client_id existe en la tabla users
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'client_id'
            """))
            
            if not result.fetchone():
                print("🔧 Agregando columna client_id a la tabla users...")
                conn.execute(text("ALTER TABLE users ADD COLUMN client_id INTEGER"))
                conn.execute(text("ALTER TABLE users ADD CONSTRAINT fk_users_client_id FOREIGN KEY (client_id) REFERENCES clients(id)"))
                conn.commit()
                print("✅ Columna client_id agregada exitosamente")
            else:
                print("✅ Columna client_id ya existe")
                
    except Exception as e:
        print(f"❌ Error actualizando estructura de base de datos: {e}")
        return False
    
    return True

def create_admin_user():
    """Crear usuario administrador"""
    print("🔐 Creando usuario administrador...")
    
    # Obtener configuración desde variables de entorno
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@ko-actuar.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_full_name = os.getenv("ADMIN_FULL_NAME", "Administrador")
    
    try:
        db = next(get_db())
        
        # Verificar si el usuario admin ya existe
        existing_admin = db.query(User).filter(User.username == admin_username).first()
        
        if existing_admin:
            print(f"✅ Usuario administrador '{admin_username}' ya existe")
            db.close()
            return True
        
        # Crear hash de la contraseña
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), salt).decode('utf-8')
        
        # Crear usuario administrador
        admin_user = User(
            username=admin_username,
            email=admin_email,
            full_name=admin_full_name,
            hashed_password=hashed_password,
            role="admin",
            is_active=True,
            client_id=None  # Admin no tiene cliente específico
        )
        
        db.add(admin_user)
        db.commit()
        
        print(f"✅ Usuario administrador creado exitosamente:")
        print(f"   Usuario: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Contraseña: {admin_password}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        return False

def create_default_client():
    """Crear cliente por defecto"""
    print("🏢 Creando cliente por defecto...")
    
    try:
        db = next(get_db())
        
        # Verificar si ya existe un cliente por defecto
        existing_client = db.query(Client).filter(Client.name == "EMPRESA PRINCIPAL").first()
        
        if existing_client:
            print("✅ Cliente por defecto ya existe")
            db.close()
            return True
        
        # Crear cliente por defecto
        default_client = Client(
            name="EMPRESA PRINCIPAL",
            description="Empresa principal del sistema - completamente configurable",
            is_active=True,
            custom_fields_config=[
                {
                    "name": "nit",
                    "label": "NIT",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Ingrese el NIT de la empresa",
                    "help_text": "Número de identificación tributaria"
                },
                {
                    "name": "programa",
                    "label": "Programa",
                    "field_type": "select",
                    "required": False,
                    "options": [
                        "Programa Estilo de Vida Saludable",
                        "Programa Seguridad Vial",
                        "Programa SGSST-ILO"
                    ],
                    "help_text": "Seleccione el programa correspondiente"
                }
            ]
        )
        
        db.add(default_client)
        db.commit()
        
        print("✅ Cliente por defecto creado exitosamente")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al crear cliente por defecto: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        return False

def main():
    """Función principal"""
    print("🚀 Actualizando Task Tracker en Railway...")
    
    try:
        # Actualizar estructura de base de datos
        if not update_database_structure():
            print("❌ Error actualizando estructura de base de datos")
            sys.exit(1)
        
        # Crear usuario administrador
        if not create_admin_user():
            print("❌ Error creando usuario administrador")
            sys.exit(1)
        
        # Crear cliente por defecto
        if not create_default_client():
            print("❌ Error creando cliente por defecto")
            sys.exit(1)
        
        print("✅ Actualización completada exitosamente")
        print("🌐 La aplicación está lista para usar")
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
