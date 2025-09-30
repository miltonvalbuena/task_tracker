#!/usr/bin/env python3
"""
Script para asignar usuarios a las tareas basándose en los datos del Excel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Task, Company
from sqlalchemy import and_

def assign_users_to_tasks():
    """Asigna usuarios a las tareas basándose en los datos del Excel"""
    
    db = SessionLocal()
    
    try:
        # Mapeo de nombres de usuarios a IDs de usuario
        user_mapping = {}
        
        # Obtener todos los usuarios
        users = db.query(User).all()
        for user in users:
            user_mapping[user.full_name] = user.id
            # También mapear variaciones del nombre
            if ' ' in user.full_name:
                first_name = user.full_name.split()[0]
                user_mapping[first_name] = user.id
        
        print(f"📋 Mapeo de usuarios creado: {len(user_mapping)} entradas")
        print("Ejemplos de mapeo:")
        for name, user_id in list(user_mapping.items())[:5]:
            print(f"   {name} -> {user_id}")
        
        # Procesar archivo COLMENA ARL
        print("\n🏢 Procesando COLMENA ARL...")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            
            # Obtener tareas de COLMENA ARL
            colmena_tasks = db.query(Task).filter(Task.company_id == 4).all()
            print(f"   Tareas encontradas en BD: {len(colmena_tasks)}")
            
            assigned_count = 0
            
            for i, task in enumerate(colmena_tasks):
                if i < len(df_colmena):
                    row = df_colmena.iloc[i]
                    
                    # Buscar usuario en las columnas de responsable
                    assigned_user_id = None
                    
                    # Columna "DIS y/o RESPONSABLE ARL"
                    if 'DIS y/o RESPONSABLE ARL' in df_colmena.columns:
                        responsable = str(row['DIS y/o RESPONSABLE ARL']).strip()
                        if responsable and responsable != 'nan' and responsable in user_mapping:
                            assigned_user_id = user_mapping[responsable]
                    
                    # Si no se encontró, buscar en "ASESOR ASIGNADO"
                    if not assigned_user_id and 'ASESOR ASIGNADO' in df_colmena.columns:
                        asesor = str(row['ASESOR ASIGNADO']).strip()
                        if asesor and asesor != 'nan' and asesor in user_mapping:
                            assigned_user_id = user_mapping[asesor]
                    
                    # Asignar usuario si se encontró
                    if assigned_user_id:
                        task.assigned_to = assigned_user_id
                        assigned_count += 1
                        print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> Usuario {assigned_user_id}")
            
            print(f"   📊 Tareas asignadas en COLMENA ARL: {assigned_count}")
        
        # Procesar archivo POSITIVA ARL
        print("\n🏢 Procesando POSITIVA ARL...")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            
            # Obtener tareas de POSITIVA ARL
            positiva_tasks = db.query(Task).filter(Task.company_id == 5).all()
            print(f"   Tareas encontradas en BD: {len(positiva_tasks)}")
            
            assigned_count = 0
            
            for i, task in enumerate(positiva_tasks):
                if i < len(df_positiva):
                    row = df_positiva.iloc[i]
                    
                    # Buscar usuario en la columna "ASESOR"
                    assigned_user_id = None
                    
                    if 'ASESOR' in df_positiva.columns:
                        asesor = str(row['ASESOR']).strip()
                        if asesor and asesor != 'nan' and asesor in user_mapping:
                            assigned_user_id = user_mapping[asesor]
                    
                    # Asignar usuario si se encontró
                    if assigned_user_id:
                        task.assigned_to = assigned_user_id
                        assigned_count += 1
                        print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> Usuario {assigned_user_id}")
            
            print(f"   📊 Tareas asignadas en POSITIVA ARL: {assigned_count}")
        
        # Confirmar cambios
        db.commit()
        
        # Verificar resultados
        print("\n📊 RESUMEN FINAL:")
        total_tasks = db.query(Task).count()
        tasks_with_users = db.query(Task).filter(Task.assigned_to.isnot(None)).count()
        
        print(f"   Total de tareas: {total_tasks}")
        print(f"   Tareas con usuario asignado: {tasks_with_users}")
        print(f"   Porcentaje asignado: {(tasks_with_users/total_tasks)*100:.1f}%")
        
        print("\n🎉 ¡Asignación de usuarios completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al asignar usuarios: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    assign_users_to_tasks()

