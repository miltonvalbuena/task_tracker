#!/usr/bin/env python3
"""
Script para actualizar los estados de las tareas según los archivos Excel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Task, User, Company
from app.schemas import TaskStatus

def update_task_status():
    """Actualiza los estados de las tareas según los archivos Excel"""
    
    db = SessionLocal()
    
    try:
        # Mapeo de estados del Excel a estados del sistema
        estado_mapping = {
            'Sin Programar': 'pendiente',
            'Programada': 'en_progreso',
            'Completada': 'completada',
            'Cancelada': 'cancelada'
        }
        
        # Procesar POSITIVA ARL (tiene columna ESTADO)
        print("🏢 Actualizando estados de POSITIVA ARL...")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            
            # Obtener tareas de POSITIVA ARL
            positiva_tasks = db.query(Task).filter(Task.company_id == 5).all()
            print(f"   Tareas encontradas en BD: {len(positiva_tasks)}")
            
            updated_count = 0
            
            for i, task in enumerate(positiva_tasks):
                if i < len(df_positiva):
                    row = df_positiva.iloc[i]
                    
                    # Obtener estado del Excel
                    if 'ESTADO' in df_positiva.columns:
                        excel_estado = str(row['ESTADO']).strip()
                        if excel_estado and excel_estado != 'nan':
                            # Mapear estado del Excel al estado del sistema
                            sistema_estado = estado_mapping.get(excel_estado, 'pendiente')
                            
                            # Actualizar estado si es diferente
                            if task.status != sistema_estado:
                                task.status = sistema_estado
                                updated_count += 1
                                print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> {sistema_estado}")
            
            print(f"   📊 Estados actualizados en POSITIVA ARL: {updated_count}")
        
        # Para COLMENA ARL, vamos a asignar estados basados en fechas y otros criterios
        print("\n🏢 Actualizando estados de COLMENA ARL...")
        colmena_tasks = db.query(Task).filter(Task.company_id == 4).all()
        print(f"   Tareas encontradas en BD: {len(colmena_tasks)}")
        
        updated_count = 0
        
        for task in colmena_tasks:
            # Lógica para asignar estados basada en fechas y otros criterios
            if task.due_date:
                from datetime import datetime, timedelta
                now = datetime.utcnow()
                due_date = task.due_date.replace(tzinfo=None) if task.due_date.tzinfo else task.due_date
                
                # Si la fecha de vencimiento ya pasó, marcar como en progreso
                if due_date < now:
                    if task.status == 'pendiente':
                        task.status = 'en_progreso'
                        updated_count += 1
                        print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> en_progreso (vencida)")
                # Si la fecha de vencimiento es próxima (dentro de 7 días), marcar como en progreso
                elif due_date <= now + timedelta(days=7):
                    if task.status == 'pendiente':
                        task.status = 'en_progreso'
                        updated_count += 1
                        print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> en_progreso (próxima a vencer)")
        
        print(f"   📊 Estados actualizados en COLMENA ARL: {updated_count}")
        
        # Confirmar cambios
        db.commit()
        
        # Verificar resultados
        print("\n📊 RESUMEN FINAL:")
        total_tasks = db.query(Task).count()
        pending_tasks = db.query(Task).filter(Task.status == 'pendiente').count()
        in_progress_tasks = db.query(Task).filter(Task.status == 'en_progreso').count()
        completed_tasks = db.query(Task).filter(Task.status == 'completada').count()
        
        print(f"   Total de tareas: {total_tasks}")
        print(f"   Pendientes: {pending_tasks}")
        print(f"   En progreso: {in_progress_tasks}")
        print(f"   Completadas: {completed_tasks}")
        
        print("\n🎉 ¡Estados de tareas actualizados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al actualizar estados: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_task_status()

