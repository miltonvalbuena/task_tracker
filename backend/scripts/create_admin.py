#!/usr/bin/env python3
"""
Script para crear usuario administrador en Railway
"""

import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Agregar el directorio padre al path para importar los modelos
sys.path.append('/app/backend')

from app.models import User

# Configuración de contraseñas
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_admin_user():
    """Crear usuario administrador"""
    print("🔐 Creando usuario administrador...")
    
    # Obtener la URL de la base de datos
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL no encontrada en variables de entorno")
        return False
    
    print(f"📊 Conectando a la base de datos...")
    
    # Intentar conectar con reintentos
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Crear engine con configuración optimizada
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "task_tracker_admin_creator"
                }
            )
            
            # Crear sesión
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            db = SessionLocal()
            
            # Verificar si el usuario admin ya existe
            existing_admin = db.query(User).filter(User.username == "admin").first()
            
            if existing_admin:
                print(f"✅ Usuario administrador 'admin' ya existe")
                print(f"   ID: {existing_admin.id}")
                print(f"   Email: {existing_admin.email}")
                print(f"   Activo: {existing_admin.is_active}")
                db.close()
                return True
            
            # Crear hash de la contraseña
            hashed_password = pwd_context.hash("admin123")
            
            # Crear usuario administrador
            admin_user = User(
                username="admin",
                email="admin@ko-actuar.com",
                full_name="Administrador",
                hashed_password=hashed_password,
                role="admin",
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            
            print(f"✅ Usuario administrador creado exitosamente:")
            print(f"   Usuario: admin")
            print(f"   Email: admin@ko-actuar.com")
            print(f"   Contraseña: admin123")
            print(f"   ID: {admin_user.id}")
            
            db.close()
            return True
            
        except Exception as e:
            print(f"❌ Error al crear usuario administrador (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print("⏳ Esperando 10 segundos antes del siguiente intento...")
                time.sleep(10)
            else:
                print("❌ No se pudo crear el usuario administrador después de todos los intentos")
                return False

def main():
    """Función principal"""
    print("🚀 Creando usuario administrador en Railway...")
    
    success = create_admin_user()
    
    if success:
        print("✅ Usuario administrador creado exitosamente")
        return True
    else:
        print("❌ Error creando usuario administrador")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
