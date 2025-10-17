#!/usr/bin/env python3
"""
Script para importar datos compatible con el esquema de Railway
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import User, Client, Task, ARL
from sqlalchemy import text, inspect

def import_railway_compatible():
    """Importar datos compatible con el esquema de Railway"""
    print("📥 Importando datos compatible con Railway...")
    
    db = SessionLocal()
    try:
        # Verificar si existe la tabla companies
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'companies' in tables:
            print("🏢 Tabla 'companies' encontrada, usando esquema de Railway")
            
            # Crear empresas basadas en los clientes
            print("🏢 Creando empresas...")
            
            # Obtener clientes existentes
            clients = db.query(Client).all()
            company_id_mapping = {}
            
            for client in clients:
                # Crear empresa para cada cliente
                company_name = client.name
                company_nit = client.nit or f"NIT-{client.id}"
                
                # Verificar si la empresa ya existe
                result = db.execute(text("SELECT id FROM companies WHERE name = :name"), {"name": company_name})
                existing_company = result.fetchone()
                
                if existing_company:
                    company_id_mapping[client.id] = existing_company[0]
                else:
                    # Crear nueva empresa
                    result = db.execute(text("""
                        INSERT INTO companies (name, nit, description, is_active, created_at) 
                        VALUES (:name, :nit, :description, :is_active, :created_at) 
                        RETURNING id
                    """), {
                        "name": company_name,
                        "nit": company_nit,
                        "description": client.description or f"Empresa {company_name}",
                        "is_active": True,
                        "created_at": datetime.now()
                    })
                    company_id = result.fetchone()[0]
                    company_id_mapping[client.id] = company_id
                    print(f"   ✅ Empresa creada: {company_name} (ID: {company_id})")
            
            db.commit()
            print(f"✅ {len(company_id_mapping)} empresas procesadas")
            
            # Crear usuarios con company_id
            print("👥 Creando usuarios con company_id...")
            
            # Datos de usuarios de ejemplo
            users_data = [
                {"email": "maria_jose@ko-actuar.com", "username": "maria_jose", "full_name": "Maria José", "client_id": 1},
                {"email": "carlos_perez@ko-actuar.com", "username": "carlos_perez", "full_name": "Carlos Pérez", "client_id": 2},
                {"email": "ana_garcia@ko-actuar.com", "username": "ana_garcia", "full_name": "Ana García", "client_id": 3}
            ]
            
            user_id_mapping = {}
            for user_data in users_data:
                client_id = user_data['client_id']
                company_id = company_id_mapping.get(client_id)
                
                if company_id:
                    # Verificar si el usuario ya existe
                    result = db.execute(text("SELECT id FROM users WHERE username = :username"), {"username": user_data['username']})
                    existing_user = result.fetchone()
                    
                    if not existing_user:
                        # Crear nuevo usuario
                        result = db.execute(text("""
                            INSERT INTO users (email, username, full_name, hashed_password, role, is_active, client_id, company_id, created_at) 
                            VALUES (:email, :username, :full_name, :hashed_password, :role, :is_active, :client_id, :company_id, :created_at) 
                            RETURNING id
                        """), {
                            "email": user_data['email'],
                            "username": user_data['username'],
                            "full_name": user_data['full_name'],
                            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K5K5K.",  # Password: password123
                            "role": "USER",
                            "is_active": True,
                            "client_id": client_id,
                            "company_id": company_id,
                            "created_at": datetime.now()
                        })
                        user_id = result.fetchone()[0]
                        user_id_mapping[user_data['username']] = user_id
                        print(f"   ✅ Usuario creado: {user_data['full_name']} (ID: {user_id})")
                    else:
                        user_id_mapping[user_data['username']] = existing_user[0]
                        print(f"   ℹ️ Usuario ya existe: {user_data['full_name']}")
            
            db.commit()
            print(f"✅ {len(user_id_mapping)} usuarios procesados")
            
            # Crear tareas
            print("📝 Creando tareas...")
            
            tasks_data = [
                {"title": "Revisión de seguridad industrial", "description": "Realizar inspección de seguridad en planta", "status": "pendiente", "priority": "alta", "due_date": "2025-11-15T00:00:00", "client_id": 1, "assigned_to": "maria_jose"},
                {"title": "Capacitación en prevención de riesgos", "description": "Capacitar personal en medidas de seguridad", "status": "en_progreso", "priority": "media", "due_date": "2025-11-20T00:00:00", "client_id": 2, "assigned_to": "carlos_perez"},
                {"title": "Actualización de protocolos", "description": "Actualizar protocolos de seguridad", "status": "completada", "priority": "baja", "due_date": "2025-10-30T00:00:00", "client_id": 3, "assigned_to": "ana_garcia"}
            ]
            
            for task_data in tasks_data:
                assigned_user_id = user_id_mapping.get(task_data['assigned_to'])
                
                if assigned_user_id:
                    # Verificar si la tarea ya existe
                    result = db.execute(text("SELECT id FROM tasks WHERE title = :title"), {"title": task_data['title']})
                    existing_task = result.fetchone()
                    
                    if not existing_task:
                        # Crear nueva tarea
                        db.execute(text("""
                            INSERT INTO tasks (title, description, status, priority, due_date, client_id, assigned_to, created_by, created_at) 
                            VALUES (:title, :description, :status, :priority, :due_date, :client_id, :assigned_to, :created_by, :created_at)
                        """), {
                            "title": task_data['title'],
                            "description": task_data['description'],
                            "status": task_data['status'],
                            "priority": task_data['priority'],
                            "due_date": datetime.fromisoformat(task_data['due_date']) if task_data['due_date'] else None,
                            "client_id": task_data['client_id'],
                            "assigned_to": assigned_user_id,
                            "created_by": assigned_user_id,
                            "created_at": datetime.now()
                        })
                        print(f"   ✅ Tarea creada: {task_data['title']}")
                    else:
                        print(f"   ℹ️ Tarea ya existe: {task_data['title']}")
            
            db.commit()
            print("✅ Tareas creadas")
            
        else:
            print("ℹ️ Tabla 'companies' no encontrada, usando esquema estándar")
            # Usar el script de importación directa normal
            import import_data_direct
            import_data_direct.import_data_direct()
        
        # Verificar importación
        print("🔍 Verificando importación...")
        
        # Contar registros usando SQL directo
        result = db.execute(text("SELECT COUNT(*) FROM tasks"))
        tasks_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        users_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) FROM clients"))
        clients_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) FROM arls"))
        arls_count = result.fetchone()[0]
        
        print(f"📊 Datos importados:")
        print(f"   - ARLs: {arls_count}")
        print(f"   - Clientes: {clients_count}")
        print(f"   - Usuarios: {users_count}")
        print(f"   - Tareas: {tasks_count}")
        
        print("✅ Importación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_railway_compatible()
