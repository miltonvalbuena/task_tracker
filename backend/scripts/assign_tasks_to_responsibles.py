#!/usr/bin/env python3
"""
Script para asignar tareas a los usuarios responsables correspondientes
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

def assign_tasks_to_responsibles():
    """Asignar tareas a los usuarios responsables correspondientes"""
    
    db = SessionLocal()
    
    try:
        # Obtener ARLs
        colmena_arl = db.query(ARL).filter(ARL.name == "COLMENA ARL").first()
        positiva_arl = db.query(ARL).filter(ARL.name == "POSITIVA ARL").first()
        
        if not colmena_arl or not positiva_arl:
            print("Error: Las ARLs no existen")
            return
        
        # Asignar tareas de COLMENA ARL
        print("=== ASIGNANDO TAREAS DE COLMENA ARL ===")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            
            assigned_count = 0
            for index, row in df_colmena.iterrows():
                try:
                    # Obtener datos de la fila
                    empresa = row['EMPRESA']
                    actividad = row['ACTIVIDAD']
                    asesor_asignado = row.get('ASESOR ASIGNADO')
                    
                    if pd.isna(empresa) or pd.isna(actividad):
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
                    if not pd.isna(asesor_asignado):
                        # Crear username del asesor
                        username = asesor_asignado.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                        
                        # Buscar el usuario
                        user = db.query(User).filter(User.username == username).first()
                        
                        if user:
                            task.assigned_to = user.id
                            assigned_count += 1
                            print(f"  ✓ Asignada: {actividad[:50]}... → {user.full_name}")
                        else:
                            print(f"  ⚠ Usuario no encontrado: {asesor_asignado}")
                    
                except Exception as e:
                    print(f"  ❌ Error procesando fila {index}: {e}")
                    continue
            
            db.commit()
            print(f"✓ Asignadas {assigned_count} tareas de COLMENA ARL")
        
        # Asignar tareas de POSITIVA ARL
        print("\n=== ASIGNANDO TAREAS DE POSITIVA ARL ===")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            
            assigned_count = 0
            for index, row in df_positiva.iterrows():
                try:
                    # Obtener datos de la fila
                    empresa = row['EMPRESA']
                    actividad = row['ACTIVIDAD']
                    asesor = row.get('ASESOR')
                    
                    if pd.isna(empresa) or pd.isna(actividad):
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
                    if not pd.isna(asesor):
                        # Crear username del asesor
                        username = f"{asesor.lower()}_positiva"
                        
                        # Buscar el usuario
                        user = db.query(User).filter(User.username == username).first()
                        
                        if user:
                            task.assigned_to = user.id
                            assigned_count += 1
                            print(f"  ✓ Asignada: {actividad[:50]}... → {user.full_name}")
                        else:
                            print(f"  ⚠ Usuario no encontrado: {asesor}")
                    
                except Exception as e:
                    print(f"  ❌ Error procesando fila {index}: {e}")
                    continue
            
            db.commit()
            print(f"✓ Asignadas {assigned_count} tareas de POSITIVA ARL")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_tasks = db.query(Task).count()
        assigned_tasks = db.query(Task).filter(Task.assigned_to.isnot(None)).count()
        unassigned_tasks = total_tasks - assigned_tasks
        
        print(f"Total de tareas: {total_tasks}")
        print(f"Tareas asignadas: {assigned_tasks}")
        print(f"Tareas sin asignar: {unassigned_tasks}")
        
        # Mostrar estadísticas por usuario
        print("\n=== TAREAS POR USUARIO ===")
        from sqlalchemy import func
        user_task_counts = db.query(
            User.full_name,
            func.count(Task.id).label('task_count')
        ).join(Task, User.id == Task.assigned_to).group_by(User.id, User.full_name).all()
        
        for user_name, task_count in user_task_counts:
            print(f"{user_name}: {task_count} tareas")
        
    except Exception as e:
        print(f"Error durante la asignación: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    assign_tasks_to_responsibles()
