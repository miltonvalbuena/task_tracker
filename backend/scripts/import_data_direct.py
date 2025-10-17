#!/usr/bin/env python3
"""
Script para importar datos directamente en Railway
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Client, Task, ARL

def import_data_direct():
    """Importar datos directamente"""
    print("📥 Importando datos directamente...")
    
    # Datos hardcodeados basados en la exportación local
    arls_data = [
        {"id": 1, "name": "COLMENA ARL", "description": "COLMENA ARL", "is_active": True},
        {"id": 2, "name": "POSITIVA ARL", "description": "POSITIVA ARL", "is_active": True},
        {"id": 3, "name": "SURA ARL", "description": "SURA ARL", "is_active": True}
    ]
    
    # Crear algunos clientes de ejemplo
    clients_data = [
        {"id": 1, "name": "AUTOMOTRIZ CALDAS MOTOR S.A.", "nit": "900123456-1", "description": "Empresa automotriz", "is_active": True, "arl_id": 1, "custom_fields_config": None},
        {"id": 2, "name": "CONSTRUCTORA EJEMPLO S.A.S.", "nit": "900234567-2", "description": "Empresa constructora", "is_active": True, "arl_id": 2, "custom_fields_config": None},
        {"id": 3, "name": "TECNOLOGIA INNOVADORA LTDA", "nit": "900345678-3", "description": "Empresa de tecnología", "is_active": True, "arl_id": 3, "custom_fields_config": None}
    ]
    
    # Crear algunos usuarios de ejemplo
    users_data = [
        {"id": 1, "email": "maria_jose@ko-actuar.com", "username": "maria_jose", "full_name": "Maria José", "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K5K5K.", "role": "user", "is_active": True, "client_id": 1},
        {"id": 2, "email": "carlos_perez@ko-actuar.com", "username": "carlos_perez", "full_name": "Carlos Pérez", "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K5K5K.", "role": "user", "is_active": True, "client_id": 2},
        {"id": 3, "email": "ana_garcia@ko-actuar.com", "username": "ana_garcia", "full_name": "Ana García", "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8K5K5K.", "role": "user", "is_active": True, "client_id": 3}
    ]
    
    # Crear algunas tareas de ejemplo
    tasks_data = [
        {"id": 1, "title": "Revisión de seguridad industrial", "description": "Realizar inspección de seguridad en planta", "status": "pendiente", "priority": "alta", "due_date": "2025-11-15T00:00:00", "completed_at": None, "client_id": 1, "assigned_to": 1, "created_by": 1, "custom_fields": None},
        {"id": 2, "title": "Capacitación en prevención de riesgos", "description": "Capacitar personal en medidas de seguridad", "status": "en_progreso", "priority": "media", "due_date": "2025-11-20T00:00:00", "completed_at": None, "client_id": 2, "assigned_to": 2, "created_by": 1, "custom_fields": None},
        {"id": 3, "title": "Actualización de protocolos", "description": "Actualizar protocolos de seguridad", "status": "completada", "priority": "baja", "due_date": "2025-10-30T00:00:00", "completed_at": "2025-10-30T10:00:00", "client_id": 3, "assigned_to": 3, "created_by": 1, "custom_fields": None}
    ]
    
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
        for arl_data in arls_data:
            arl = ARL(
                name=arl_data['name'],
                description=arl_data['description'],
                is_active=arl_data['is_active']
            )
            db.add(arl)
            db.flush()
            arl_id_mapping[arl_data['id']] = arl.id
        db.commit()
        print(f"✅ {len(arls_data)} ARLs importadas")
        
        # Importar Clientes
        print("🏢 Importando Clientes...")
        client_id_mapping = {}
        for client_data in clients_data:
            client = Client(
                name=client_data['name'],
                nit=client_data['nit'],
                description=client_data['description'],
                is_active=client_data['is_active'],
                arl_id=arl_id_mapping.get(client_data['arl_id']),
                custom_fields_config=client_data['custom_fields_config']
            )
            db.add(client)
            db.flush()
            client_id_mapping[client_data['id']] = client.id
        db.commit()
        print(f"✅ {len(clients_data)} Clientes importados")
        
        # Importar Usuarios
        print("👥 Importando Usuarios...")
        user_id_mapping = {}
        for user_data in users_data:
            user = User(
                email=user_data['email'],
                username=user_data['username'],
                full_name=user_data['full_name'],
                hashed_password=user_data['hashed_password'],
                role=user_data['role'],
                is_active=user_data['is_active'],
                client_id=client_id_mapping.get(user_data['client_id'])
            )
            db.add(user)
            db.flush()
            user_id_mapping[user_data['id']] = user.id
        db.commit()
        print(f"✅ {len(users_data)} Usuarios importados")
        
        # Importar Tareas
        print("📝 Importando Tareas...")
        for task_data in tasks_data:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                priority=task_data['priority'],
                due_date=datetime.fromisoformat(task_data['due_date']) if task_data['due_date'] else None,
                completed_at=datetime.fromisoformat(task_data['completed_at']) if task_data['completed_at'] else None,
                client_id=client_id_mapping.get(task_data['client_id']),
                assigned_to=user_id_mapping.get(task_data['assigned_to']),
                created_by=user_id_mapping.get(task_data['created_by']),
                custom_fields=task_data['custom_fields']
            )
            db.add(task)
        db.commit()
        print(f"✅ {len(tasks_data)} Tareas importadas")
        
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
    import_data_direct()
