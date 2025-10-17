#!/usr/bin/env python3
"""
Script para importar EXACTAMENTE todos los datos locales a Railway
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import User, Client, Task, ARL
from sqlalchemy import text, inspect

def import_exact_local_data():
    """Importar EXACTAMENTE todos los datos locales a Railway"""
    print("📥 Importando EXACTAMENTE todos los datos locales a Railway...")
    
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
    
    print(f"📊 Datos a importar:")
    print(f"   - ARLs: {data['summary']['total_arls']}")
    print(f"   - Clientes: {data['summary']['total_clients']}")
    print(f"   - Usuarios: {data['summary']['total_users']}")
    print(f"   - Tareas: {data['summary']['total_tasks']}")
    
    db = SessionLocal()
    try:
        # Verificar esquema de Railway
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"🔍 Tablas en Railway: {tables}")
        
        # Limpiar datos existentes (excepto admin)
        print("🧹 Limpiando datos existentes...")
        db.execute(text("DELETE FROM tasks"))
        db.execute(text("DELETE FROM users WHERE username != 'admin'"))
        db.execute(text("DELETE FROM clients"))
        db.execute(text("DELETE FROM arls"))
        if 'companies' in tables:
            db.execute(text("DELETE FROM companies"))
        db.commit()
        print("✅ Datos existentes eliminados")
        
        # Importar ARLs
        print("📋 Importando ARLs...")
        arl_id_mapping = {}
        for arl_data in data['arls']:
            arl = ARL(
                name=arl_data['name'],
                description=arl_data['description'],
                is_active=arl_data['is_active']
            )
            db.add(arl)
            db.flush()
            arl_id_mapping[arl_data['id']] = arl.id
        db.commit()
        print(f"✅ {len(data['arls'])} ARLs importadas")
        
        # Importar Clientes
        print("🏢 Importando Clientes...")
        client_id_mapping = {}
        for client_data in data['clients']:
            client = Client(
                name=client_data['name'],
                nit=client_data['nit'],
                description=client_data['description'],
                is_active=client_data['is_active'],
                arl_id=arl_id_mapping.get(client_data['arl_id']) if client_data['arl_id'] else None,
                custom_fields_config=client_data['custom_fields_config']
            )
            db.add(client)
            db.flush()
            client_id_mapping[client_data['id']] = client.id
        db.commit()
        print(f"✅ {len(data['clients'])} Clientes importados")
        
        # Crear empresas si existe la tabla companies
        company_id_mapping = {}
        if 'companies' in tables:
            print("🏢 Creando empresas para Railway...")
            for client_data in data['clients']:
                client_id = client_id_mapping.get(client_data['id'])
                if client_id:
                    # Crear empresa para cada cliente
                    result = db.execute(text("""
                        INSERT INTO companies (name, nit, description, is_active, created_at) 
                        VALUES (:name, :nit, :description, :is_active, :created_at) 
                        RETURNING id
                    """), {
                        "name": client_data['name'],
                        "nit": client_data['nit'] or f"NIT-{client_id}",
                        "description": client_data['description'] or f"Empresa {client_data['name']}",
                        "is_active": True,
                        "created_at": datetime.now()
                    })
                    company_id = result.fetchone()[0]
                    company_id_mapping[client_id] = company_id
            db.commit()
            print(f"✅ {len(company_id_mapping)} Empresas creadas")
        
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
            
            # Crear usuario usando SQL directo para manejar company_id
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
                    "role": user_data['role'],
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
                    role=user_data['role'],
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
        arls_count = db.query(ARL).count()
        clients_count = db.query(Client).count()
        users_count = db.query(User).count()
        tasks_count = db.query(Task).count()
        
        print(f"📊 Datos importados:")
        print(f"   - ARLs: {arls_count}")
        print(f"   - Clientes: {clients_count}")
        print(f"   - Usuarios: {users_count}")
        print(f"   - Tareas: {tasks_count}")
        
        # Verificar que coinciden con los datos originales
        if (arls_count == data['summary']['total_arls'] and 
            clients_count == data['summary']['total_clients'] and 
            users_count == data['summary']['total_users'] and 
            tasks_count == data['summary']['total_tasks']):
            print("✅ ¡TODOS los datos se importaron correctamente!")
        else:
            print("⚠️ Algunos datos no coinciden con la exportación original")
        
        print("✅ Importación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_exact_local_data()
