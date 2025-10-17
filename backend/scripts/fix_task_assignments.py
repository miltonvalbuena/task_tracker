#!/usr/bin/env python3
"""
Script para corregir las asignaciones de tareas basándose en los asesores reales de los archivos Excel
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

def fix_task_assignments():
    """Corregir las asignaciones de tareas basándose en los asesores reales"""
    
    db = SessionLocal()
    
    try:
        # Obtener ARLs
        colmena_arl = db.query(ARL).filter(ARL.name == "COLMENA ARL").first()
        positiva_arl = db.query(ARL).filter(ARL.name == "POSITIVA ARL").first()
        
        if not colmena_arl or not positiva_arl:
            print("Error: Las ARLs no existen")
            return
        
        print("=== CORRIGIENDO ASIGNACIONES DE TAREAS ===")
        
        # Primero, limpiar todas las asignaciones incorrectas
        print("\n1. Limpiando asignaciones incorrectas...")
        incorrect_users = ['user_colmena', 'user_positiva', 'user_sura', 'manager_colmena', 'manager_positiva', 'manager_sura']
        
        for username in incorrect_users:
            user = db.query(User).filter(User.username == username).first()
            if user:
                tasks_to_clear = db.query(Task).filter(Task.assigned_to == user.id).all()
                for task in tasks_to_clear:
                    task.assigned_to = None
                print(f"  ✓ Limpiadas {len(tasks_to_clear)} tareas asignadas incorrectamente a {username}")
        
        db.commit()
        
        # Crear usuarios reales para los asesores si no existen
        print("\n2. Creando/verificando usuarios reales...")
        
        # Obtener clientes por defecto
        colmena_client = db.query(Client).filter(Client.arl_id == colmena_arl.id).first()
        positiva_client = db.query(Client).filter(Client.arl_id == positiva_arl.id).first()
        
        # Asesores de Colmena
        colmena_asesores = ['Otoniel', 'Maria José', 'Gisela', 'Manuela', 'Ana', 'Diana', 'Luz', 'Carlos Eduardo']
        for asesor in colmena_asesores:
            username = asesor.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            existing_user = db.query(User).filter(User.username == username).first()
            
            if not existing_user:
                user = User(
                    username=username,
                    email=f"{username}@colmena.com",
                    full_name=asesor,
                    hashed_password=get_password_hash("user123"),
                    role=UserRole.USER,
                    client_id=colmena_client.id,
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Creado usuario: {asesor} ({username})")
            else:
                print(f"  - Usuario ya existe: {asesor} ({username})")
        
        # Asesores de Positiva
        positiva_asesores = ['Carlos', 'Maria José', 'Luz', 'Ana', 'Otoniel']
        for asesor in positiva_asesores:
            username = f"{asesor.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_positiva"
            existing_user = db.query(User).filter(User.username == username).first()
            
            if not existing_user:
                user = User(
                    username=username,
                    email=f"{username}@positiva.com",
                    full_name=asesor,
                    hashed_password=get_password_hash("user123"),
                    role=UserRole.USER,
                    client_id=positiva_client.id,
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Creado usuario: {asesor} ({username})")
            else:
                print(f"  - Usuario ya existe: {asesor} ({username})")
        
        db.commit()
        
        # Ahora reasignar las tareas correctamente
        print("\n3. Reasignando tareas basándose en los archivos Excel...")
        
        # Procesar archivo de Colmena
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            print(f"\n--- Procesando {len(df_colmena)} actividades de COLMENA ARL ---")
            
            assigned_count = 0
            for index, row in df_colmena.iterrows():
                try:
                    empresa = row.get('EMPRESA')
                    actividad = row.get('ACTIVIDAD')
                    asesor_asignado = row.get('ASESOR ASIGNADO')
                    
                    if pd.isna(empresa) or pd.isna(actividad) or pd.isna(asesor_asignado):
                        continue
                    
                    # Buscar el cliente
                    client = db.query(Client).filter(
                        Client.name == empresa,
                        Client.arl_id == colmena_arl.id
                    ).first()
                    
                    if not client:
                        continue
                    
                    # Buscar la tarea
                    task = db.query(Task).filter(
                        Task.title.like(f"%{actividad[:50]}%"),
                        Task.client_id == client.id
                    ).first()
                    
                    if not task:
                        continue
                    
                    # Buscar el usuario asesor
                    username = str(asesor_asignado).lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                    user = db.query(User).filter(User.username == username).first()
                    
                    if user:
                        task.assigned_to = user.id
                        assigned_count += 1
                        if assigned_count <= 10:  # Mostrar solo las primeras 10
                            print(f"  ✓ {actividad[:40]}... → {user.full_name}")
                    else:
                        print(f"  ⚠ Usuario no encontrado: {asesor_asignado} ({username})")
                        
                except Exception as e:
                    print(f"  ❌ Error procesando fila {index}: {e}")
                    continue
            
            print(f"  ✓ Total asignadas en Colmena: {assigned_count}")
        
        # Procesar archivo de Positiva
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            print(f"\n--- Procesando {len(df_positiva)} actividades de POSITIVA ARL ---")
            
            assigned_count = 0
            for index, row in df_positiva.iterrows():
                try:
                    empresa = row.get('EMPRESA')
                    actividad = row.get('ACTIVIDAD')
                    asesor = row.get('ASESOR')
                    
                    if pd.isna(empresa) or pd.isna(actividad) or pd.isna(asesor):
                        continue
                    
                    # Buscar el cliente
                    client = db.query(Client).filter(
                        Client.name == empresa,
                        Client.arl_id == positiva_arl.id
                    ).first()
                    
                    if not client:
                        continue
                    
                    # Buscar la tarea
                    task = db.query(Task).filter(
                        Task.title.like(f"%{actividad[:50]}%"),
                        Task.client_id == client.id
                    ).first()
                    
                    if not task:
                        continue
                    
                    # Buscar el usuario asesor
                    username = f"{str(asesor).lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_positiva"
                    user = db.query(User).filter(User.username == username).first()
                    
                    if user:
                        task.assigned_to = user.id
                        assigned_count += 1
                        if assigned_count <= 10:  # Mostrar solo las primeras 10
                            print(f"  ✓ {actividad[:40]}... → {user.full_name}")
                    else:
                        print(f"  ⚠ Usuario no encontrado: {asesor} ({username})")
                        
                except Exception as e:
                    print(f"  ❌ Error procesando fila {index}: {e}")
                    continue
            
            print(f"  ✓ Total asignadas en Positiva: {assigned_count}")
        
        db.commit()
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_tasks = db.query(Task).count()
        assigned_tasks = db.query(Task).filter(Task.assigned_to.isnot(None)).count()
        unassigned_tasks = total_tasks - assigned_tasks
        
        print(f"Total de tareas: {total_tasks}")
        print(f"Tareas asignadas: {assigned_tasks}")
        print(f"Tareas sin asignar: {unassigned_tasks}")
        
        # Mostrar estadísticas por usuario
        print("\n=== TAREAS POR USUARIO REAL ===")
        from sqlalchemy import func
        user_task_counts = db.query(
            User.full_name,
            User.username,
            User.email,
            func.count(Task.id).label('task_count')
        ).join(Task, User.id == Task.assigned_to).group_by(User.id, User.full_name, User.username, User.email).order_by(func.count(Task.id).desc()).all()
        
        for user_name, username, email, task_count in user_task_counts:
            print(f"  • {user_name} ({username}) - {email}: {task_count} tareas")
        
    except Exception as e:
        print(f"Error durante la corrección: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_task_assignments()
