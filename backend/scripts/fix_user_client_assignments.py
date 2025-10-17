#!/usr/bin/env python3
"""
Script para corregir las asignaciones de usuarios a clientes específicos
basándose en las tareas que realmente tienen asignadas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, ARL, Client, User, Task, TaskStatus, TaskPriority, UserRole
from app.auth import get_password_hash
from datetime import datetime, timedelta

def fix_user_client_assignments():
    """Corregir las asignaciones de usuarios a clientes específicos"""
    
    db = SessionLocal()
    
    try:
        print("=== CORRIGIENDO ASIGNACIONES DE USUARIOS A CLIENTES ===")
        
        # Obtener todas las tareas asignadas
        assigned_tasks = db.query(Task).filter(Task.assigned_to.isnot(None)).all()
        
        print(f"Procesando {len(assigned_tasks)} tareas asignadas...")
        
        # Crear un diccionario para mapear asesor -> empresas donde tiene tareas
        asesor_empresas = {}
        
        for task in assigned_tasks:
            if task.assigned_to and task.client:
                user = db.query(User).filter(User.id == task.assigned_to).first()
                if user:
                    asesor_name = user.full_name
                    empresa_name = task.client.name
                    
                    if asesor_name not in asesor_empresas:
                        asesor_empresas[asesor_name] = set()
                    asesor_empresas[asesor_name].add(empresa_name)
        
        print(f"\nAsesores y empresas donde tienen tareas:")
        for asesor, empresas in asesor_empresas.items():
            print(f"  • {asesor}: {len(empresas)} empresas")
            for empresa in empresas:
                print(f"    - {empresa[:50]}...")
        
        # Ahora crear usuarios específicos para cada asesor en cada empresa
        print(f"\n=== CREANDO USUARIOS ESPECÍFICOS POR EMPRESA ===")
        
        users_created = 0
        for asesor_name, empresas in asesor_empresas.items():
            for empresa_name in empresas:
                # Crear username específico: asesor_empresa
                empresa_short = empresa_name.replace(' ', '_').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '_')[:20]
                username = f"{asesor_name.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_{empresa_short}"
                
                # Verificar si ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    print(f"  - Usuario ya existe: {username}")
                    continue
                
                # Buscar el cliente
                client = db.query(Client).filter(Client.name == empresa_name).first()
                if not client:
                    print(f"  ⚠ Cliente no encontrado: {empresa_name}")
                    continue
                
                # Crear el usuario específico
                user = User(
                    username=username,
                    email=f"{username}@{client.arl.name.lower().replace(' ', '')}.com",
                    full_name=f"{asesor_name} - {empresa_name[:30]}",
                    hashed_password=get_password_hash("user123"),
                    role=UserRole.USER,
                    client_id=client.id,
                    is_active=True
                )
                db.add(user)
                users_created += 1
                print(f"  ✓ Creado: {username} para {empresa_name[:40]}...")
        
        db.commit()
        print(f"\n✓ Creados {users_created} usuarios específicos por empresa")
        
        # Ahora reasignar las tareas a los usuarios específicos
        print(f"\n=== REASIGNANDO TAREAS A USUARIOS ESPECÍFICOS ===")
        
        reassigned_count = 0
        for task in assigned_tasks:
            if task.assigned_to and task.client:
                # Obtener el usuario actual
                current_user = db.query(User).filter(User.id == task.assigned_to).first()
                if not current_user:
                    continue
                
                # Buscar el usuario específico para esta empresa
                asesor_name = current_user.full_name.split(' - ')[0]  # Obtener solo el nombre del asesor
                empresa_short = task.client.name.replace(' ', '_').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '_')[:20]
                specific_username = f"{asesor_name.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_{empresa_short}"
                
                specific_user = db.query(User).filter(User.username == specific_username).first()
                if specific_user:
                    task.assigned_to = specific_user.id
                    reassigned_count += 1
                    if reassigned_count <= 10:  # Mostrar solo las primeras 10
                        print(f"  ✓ {task.title[:40]}... → {specific_user.full_name}")
        
        db.commit()
        print(f"✓ Reasignadas {reassigned_count} tareas a usuarios específicos")
        
        # Mostrar resumen final
        print(f"\n=== RESUMEN FINAL ===")
        total_users = db.query(User).count()
        total_tasks = db.query(Task).count()
        assigned_tasks = db.query(Task).filter(Task.assigned_to.isnot(None)).count()
        
        print(f"Total de usuarios: {total_users}")
        print(f"Total de tareas: {total_tasks}")
        print(f"Tareas asignadas: {assigned_tasks}")
        
        # Verificar que las asignaciones coincidan
        print(f"\n=== VERIFICACIÓN DE ASIGNACIONES ===")
        correct_assignments = 0
        incorrect_assignments = 0
        
        for task in db.query(Task).filter(Task.assigned_to.isnot(None)).limit(10).all():
            user = db.query(User).filter(User.id == task.assigned_to).first()
            if user and user.client and task.client:
                if user.client.id == task.client.id:
                    correct_assignments += 1
                    print(f"  ✅ {task.title[:30]}... → {user.full_name[:30]}... (Cliente coincide)")
                else:
                    incorrect_assignments += 1
                    print(f"  ❌ {task.title[:30]}... → {user.full_name[:30]}... (Cliente NO coincide)")
        
        print(f"\nAsignaciones correctas: {correct_assignments}")
        print(f"Asignaciones incorrectas: {incorrect_assignments}")
        
    except Exception as e:
        print(f"Error durante la corrección: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user_client_assignments()
