#!/usr/bin/env python3
"""
Script para importar datos exportados a Railway
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Client, Task, ARL
from app.auth import get_password_hash

def import_to_railway(export_file):
    """Importar datos exportados a Railway"""
    print(f"📥 Importando datos desde: {export_file}")
    
    # Leer archivo de exportación
    with open(export_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Datos a importar:")
    print(f"   - ARLs: {data['summary']['total_arls']}")
    print(f"   - Clientes: {data['summary']['total_clients']}")
    print(f"   - Usuarios: {data['summary']['total_users']}")
    print(f"   - Tareas: {data['summary']['total_tasks']}")
    
    db = SessionLocal()
    try:
        # Limpiar datos existentes (excepto admin)
        print("🧹 Limpiando datos existentes...")
        db.query(Task).delete()
        db.query(User).filter(User.username != "admin").delete()
        db.query(Client).delete()
        db.query(ARL).delete()
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
            db.flush()  # Para obtener el nuevo ID
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
            db.flush()  # Para obtener el nuevo ID
            client_id_mapping[client_data['id']] = client.id
        db.commit()
        print(f"✅ {len(data['clients'])} Clientes importados")
        
        # Importar Usuarios
        print("👥 Importando Usuarios...")
        user_id_mapping = {}
        for user_data in data['users']:
            # Saltar el usuario admin existente
            if user_data['username'] == 'admin':
                user_id_mapping[user_data['id']] = db.query(User).filter(User.username == 'admin').first().id
                continue
                
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
            db.flush()  # Para obtener el nuevo ID
            user_id_mapping[user_data['id']] = user.id
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
        
        print("✅ Importación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error importando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python import_to_railway.py <archivo_exportacion.json>")
        sys.exit(1)
    
    export_file = sys.argv[1]
    import_to_railway(export_file)
