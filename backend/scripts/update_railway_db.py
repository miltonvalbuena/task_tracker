#!/usr/bin/env python3
"""
Script para actualizar la base de datos en Railway
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, User, Client, Task, ARL
from app.auth import get_password_hash
from sqlalchemy import text

def update_railway_db():
    """Actualizar la base de datos en Railway"""
    print("🔧 Actualizando base de datos en Railway...")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas o ya existen")
    
    db = SessionLocal()
    try:
        # Verificar si existe el usuario admin
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            print("👤 Creando usuario administrador...")
            admin_user = User(
                username="admin",
                email="admin@ko-actuar.com",
                full_name="Administrador",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True,
                client_id=None  # Admin no tiene cliente asignado
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuario administrador creado")
        else:
            print("✅ Usuario administrador ya existe")
            
        # Verificar si hay clientes
        clients_count = db.query(Client).count()
        print(f"📊 Clientes en la base de datos: {clients_count}")
        
        # Verificar si hay tareas
        tasks_count = db.query(Task).count()
        print(f"📋 Tareas en la base de datos: {tasks_count}")
        
        # Verificar si hay usuarios
        users_count = db.query(User).count()
        print(f"👥 Usuarios en la base de datos: {users_count}")
        
        print("✅ Base de datos actualizada correctamente")
        
    except Exception as e:
        print(f"❌ Error actualizando base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_railway_db()