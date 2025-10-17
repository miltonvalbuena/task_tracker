#!/usr/bin/env python3
"""
Script para importar solo usuarios y tareas (asumiendo que ARLs y Clientes ya están)
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import User, Client, Task, ARL
from sqlalchemy import text, inspect

def import_users_tasks_only():
    """Importar solo usuarios y tareas"""
    print("📥 Importando usuarios y tareas...")
    
    # Buscar el archivo de exportación más reciente
    export_files = [f for f in os.listdir('/app/backend') if f.startswith('complete_local_data_export_') and f.endswith('.json')]
    if not export_files:
        print("❌ No se encontró archivo de exportación local")
        return
    
    latest_export = sorted(export_files)[-1]
    print(f"📁 Usando archivo de exportación: {latest_export}")
    
    # Leer archivo de exportación
    with open(f'/app/backend/{latest_export}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    db = SessionLocal()
    try:
        # Verificar esquema de Railway
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Obtener mapeos existentes
        print("🔍 Obteniendo mapeos existentes...")
        
        # Mapeo de clientes
        clients = db.query(Client).all()
        client_id_mapping = {}
        for client in clients:
            # Buscar el cliente original por nombre
            for client_data in data['clients']:
                if client.name == client_data['name']:
                    client_id_mapping[client_data['id']] = client.id
                    break
        
        print(f"✅ {len(client_id_mapping)} clientes mapeados")
        
        # Mapeo de empresas si existe
        company_id_mapping = {}
        if 'companies' in tables:
            result = db.execute(text("SELECT id, name FROM companies"))
            companies = result.fetchall()
            for company in companies:
                company_id, company_name = company
                # Buscar el cliente correspondiente
                for client_data in data['clients']:
                    if client_data['name'] == company_name:
                        client_id = client_id_mapping.get(client_data['id'])
                        if client_id:
                            company_id_mapping[client_id] = company_id
                        break
        
        # Limpiar usuarios y tareas existentes
        print("🧹 Limpiando usuarios y tareas existentes...")
        db.execute(text("DELETE FROM tasks"))
        db.execute(text("DELETE FROM users WHERE username != 'admin'"))
        db.commit()
        print("✅ Usuarios y tareas existentes eliminados")
        
        # Importar Usuarios
        print("👥 Importando Usuarios...")
        user_id_mapping = {}
        for user_data in data['users']:
            # Saltar el usuario admin existente
            if user_data['username'] == 'admin':
                admin_user = db.query(User).filter(User.username == 'admin').first()
                if admin_user:
                    user_id_mapping[user_data['id']] = admin_user.id
                continue
            
            # Obtener company_id si existe la tabla companies
            company_id = None
            if 'companies' in tables and user_data['client_id']:
                client_id = client_id_mapping.get(user_data['client_id'])
                company_id = company_id_mapping.get(client_id)
            
            # Crear usuario usando SQL directo
            if 'companies' in tables and company_id:
                result = db.execute(text("""
                    INSERT INTO users (email, username, full_name, hashed_password, role, is_active, client_id, company_id, created_at) 
                    VALUES (:email, :username, :full_name, :hashed_password, :role, :is_active, :client_id, :company_id, :created_at) 
                    RETURNING id
                """), {
                    "email": user_data['email'],
                    "username": user_data['username'],
                    "full_name": user_data['full_name'],
                    "hashed_password": user_data['hashed_password'],
                    "role": "USER",  # Forzar a USER en mayúscula
                    "is_active": user_data['is_active'],
                    "client_id": client_id_mapping.get(user_data['client_id']) if user_data['client_id'] else None,
                    "company_id": company_id,
                    "created_at": datetime.now()
                })
                user_id = result.fetchone()[0]
            else:
                # Usar modelo normal si no hay tabla companies
                user = User(
                    email=user_data['email'],
                    username=user_data['username'],
                    full_name=user_data['full_name'],
                    hashed_password=user_data['hashed_password'],
                    role="USER",  # Forzar a USER en mayúscula
                    is_active=user_data['is_active'],
                    client_id=client_id_mapping.get(user_data['client_id']) if user_data['client_id'] else None
                )
                db.add(user)
                db.flush()
                user_id = user.id
            
            user_id_mapping[user_data['id']] = user_id
        
        db.commit()
        print(f"✅ {len(data['users'])} Usuarios importados")
        
        # Importar Tareas
        print("📝 Importando Tareas...")
        for task_data in data['tasks']:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                priority=task_data['priority'],
                due_date=datetime.fromisoformat(task_data['due_date']) if task_data['due_date'] else None,
                completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data['completed_at'] else None,
                client_id=client_id_mapping.get(task_data['client_id']) if task_data['client_id'] else None,
                assigned_to=user_id_mapping.get(task_data['assigned_to']) if task_data['assigned_to'] else None,
                created_by=user_id_mapping.get(task_data['created_by']) if task_data['created_by'] else None,
                custom_fields=task_data['custom_fields']
            )
            db.add(task)
        db.commit()
        print(f"✅ {len(data['tasks'])} Tareas importadas")
        
        # Verificar importación
        print("🔍 Verificando importación...")
        users_count = db.query(User).count()
        tasks_count = db.query(Task).count()
        
        print(f"📊 Datos importados:")
        print(f"   - Usuarios: {users_count}")
        print(f"   - Tareas: {tasks_count}")
        
        # Verificar que coinciden con los datos originales
        if (users_count == data['summary']['total_users'] and 
            tasks_count == data['summary']['total_tasks']):
            print("✅ ¡TODOS los usuarios y tareas se importaron correctamente!")
        else:
            print(f"⚠️ Algunos datos no coinciden:")
            print(f"   - Usuarios esperados: {data['summary']['total_users']}, importados: {users_count}")
            print(f"   - Tareas esperadas: {data['summary']['total_tasks']}, importadas: {tasks_count}")
        
        print("✅ Importación de usuarios y tareas completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error importando usuarios y tareas: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_users_tasks_only()
