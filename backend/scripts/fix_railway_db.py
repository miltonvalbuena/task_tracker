#!/usr/bin/env python3
"""
Script para corregir la base de datos en Railway
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, User, Client, Task, ARL
from app.auth import get_password_hash
from sqlalchemy import text, inspect

def fix_railway_db():
    """Corregir la base de datos en Railway"""
    print("🔧 Corrigiendo base de datos en Railway...")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas o ya existen")
    
    # Verificar estructura de las tablas
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"📊 Tablas en la base de datos: {tables}")
    
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
                client_id=None
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
        try:
            tasks_count = db.query(Task).count()
            print(f"📋 Tareas en la base de datos: {tasks_count}")
        except Exception as e:
            print(f"❌ Error consultando tareas: {e}")
            # Intentar recrear la tabla de tareas
            print("🔄 Recreando tabla de tareas...")
            Task.__table__.drop(engine, checkfirst=True)
            Task.__table__.create(engine)
            print("✅ Tabla de tareas recreada")
        
        # Verificar si hay usuarios
        users_count = db.query(User).count()
        print(f"👥 Usuarios en la base de datos: {users_count}")
        
        # Verificar esquema de la base de datos
        print("🔍 Verificando esquema de la base de datos...")
        try:
            import check_railway_schema
            check_railway_schema.check_railway_schema()
        except Exception as e:
            print(f"⚠️ Error verificando esquema: {e}")
        
        # Importar EXACTAMENTE todos los datos locales
        print("📥 Importando EXACTAMENTE todos los datos locales...")
        try:
            import import_exact_local_data
            import_exact_local_data.import_exact_local_data()
            print("✅ TODOS los datos locales importados exitosamente")
        except Exception as e:
            print(f"⚠️ Error importando datos locales: {e}")
        
        print("✅ Base de datos corregida correctamente")
        
    except Exception as e:
        print(f"❌ Error corrigiendo base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_railway_db()
