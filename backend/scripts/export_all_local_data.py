#!/usr/bin/env python3
"""
Script para exportar TODOS los datos de la base de datos local
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Client, Task, ARL

def export_all_local_data():
    """Exportar TODOS los datos de la base de datos local"""
    print("📤 Exportando TODOS los datos de la base de datos local...")
    
    db = SessionLocal()
    try:
        # Exportar ARLs
        print("📋 Exportando ARLs...")
        arls = db.query(ARL).all()
        arls_data = []
        for arl in arls:
            arls_data.append({
                'id': arl.id,
                'name': arl.name,
                'description': arl.description,
                'is_active': arl.is_active,
                'created_at': arl.created_at.isoformat() if arl.created_at else None,
                'updated_at': arl.updated_at.isoformat() if arl.updated_at else None
            })
        
        # Exportar Clientes
        print("🏢 Exportando Clientes...")
        clients = db.query(Client).all()
        clients_data = []
        for client in clients:
            clients_data.append({
                'id': client.id,
                'name': client.name,
                'nit': client.nit,
                'description': client.description,
                'is_active': client.is_active,
                'arl_id': client.arl_id,
                'custom_fields_config': client.custom_fields_config,
                'created_at': client.created_at.isoformat() if client.created_at else None,
                'updated_at': client.updated_at.isoformat() if client.updated_at else None
            })
        
        # Exportar Usuarios
        print("👥 Exportando Usuarios...")
        users = db.query(User).all()
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'full_name': user.full_name,
                'hashed_password': user.hashed_password,
                'role': user.role,
                'is_active': user.is_active,
                'client_id': user.client_id,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            })
        
        # Exportar Tareas
        print("📝 Exportando Tareas...")
        tasks = db.query(Task).all()
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'client_id': task.client_id,
                'assigned_to': task.assigned_to,
                'created_by': task.created_by,
                'custom_fields': task.custom_fields,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'updated_at': task.updated_at.isoformat() if task.updated_at else None
            })
        
        # Crear archivo de exportación completo
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'source': 'local_database',
            'arls': arls_data,
            'clients': clients_data,
            'users': users_data,
            'tasks': tasks_data,
            'summary': {
                'total_arls': len(arls_data),
                'total_clients': len(clients_data),
                'total_users': len(users_data),
                'total_tasks': len(tasks_data)
            }
        }
        
        # Guardar en archivo JSON
        export_filename = f"complete_local_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(export_filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ TODOS los datos exportados exitosamente a: {export_filename}")
        print(f"📊 Resumen de exportación:")
        print(f"   - ARLs: {len(arls_data)}")
        print(f"   - Clientes: {len(clients_data)}")
        print(f"   - Usuarios: {len(users_data)}")
        print(f"   - Tareas: {len(tasks_data)}")
        
        # Mostrar algunos ejemplos
        print(f"\n📋 Ejemplos de datos exportados:")
        if arls_data:
            print(f"   ARL ejemplo: {arls_data[0]['name']}")
        if clients_data:
            print(f"   Cliente ejemplo: {clients_data[0]['name']}")
        if users_data:
            print(f"   Usuario ejemplo: {users_data[0]['full_name']} ({users_data[0]['email']})")
        if tasks_data:
            print(f"   Tarea ejemplo: {tasks_data[0]['title']}")
        
        return export_filename
        
    except Exception as e:
        print(f"❌ Error exportando datos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    export_all_local_data()
