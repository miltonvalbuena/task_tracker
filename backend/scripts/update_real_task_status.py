#!/usr/bin/env python3
"""
Script para actualizar los estados reales de las tareas basándose en los archivos Excel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Task, User, Company
from app.schemas import TaskStatus
import re

def update_real_task_status():
    """Actualiza los estados reales de las tareas basándose en los archivos Excel"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Analizando archivos Excel para determinar estados reales...")
        
        # Procesar COLMENA ARL
        print("\n🏢 Procesando COLMENA ARL...")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            
            # Obtener tareas de COLMENA ARL
            colmena_tasks = db.query(Task).filter(Task.company_id == 4).all()
            print(f"   Tareas encontradas en BD: {len(colmena_tasks)}")
            
            completed_count = 0
            in_progress_count = 0
            pending_count = 0
            
            for i, task in enumerate(colmena_tasks):
                if i < len(df_colmena):
                    row = df_colmena.iloc[i]
                    
                    # Determinar estado basado en horas pendientes y observaciones
                    horas_pendientes = row.get('HORAS PENDIENTES POR EJECUTAR', 0)
                    observaciones = str(row.get('OBSERVACIONES', '')).strip()
                    
                    # Si tiene 0 horas pendientes, está completada
                    if horas_pendientes == 0:
                        if task.status != 'completada':
                            task.status = 'completada'
                            completed_count += 1
                            print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> COMPLETADA (0 horas pendientes)")
                    
                    # Si tiene observaciones con "FACTURADA", está completada
                    elif 'FACTURADA' in observaciones.upper():
                        if task.status != 'completada':
                            task.status = 'completada'
                            completed_count += 1
                            print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> COMPLETADA (FACTURADA)")
                    
                    # Si tiene observaciones con fechas de ejecución, está en progreso
                    elif re.search(r'\d{1,2}[A-Za-z]{3}\s*\(\d+H\)', observaciones) or 'AUTORIZACIÓN' in observaciones.upper():
                        if task.status != 'en_progreso':
                            task.status = 'en_progreso'
                            in_progress_count += 1
                            print(f"   🔄 Tarea {task.id}: {task.title[:30]}... -> EN PROGRESO (con ejecución)")
                    
                    # Si tiene horas pendientes > 0 y no tiene ejecución, está pendiente
                    elif horas_pendientes > 0:
                        if task.status != 'pendiente':
                            task.status = 'pendiente'
                            pending_count += 1
                            print(f"   ⏳ Tarea {task.id}: {task.title[:30]}... -> PENDIENTE")
            
            print(f"   📊 COLMENA ARL - Completadas: {completed_count}, En progreso: {in_progress_count}, Pendientes: {pending_count}")
        
        # Procesar POSITIVA ARL
        print("\n🏢 Procesando POSITIVA ARL...")
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
                            if excel_estado == 'Sin Programar':
                                sistema_estado = 'pendiente'
                            elif excel_estado == 'Programada':
                                sistema_estado = 'en_progreso'
                            else:
                                sistema_estado = 'pendiente'
                            
                            # Actualizar estado si es diferente
                            if task.status != sistema_estado:
                                task.status = sistema_estado
                                updated_count += 1
                                print(f"   ✅ Tarea {task.id}: {task.title[:30]}... -> {sistema_estado}")
            
            print(f"   📊 Estados actualizados en POSITIVA ARL: {updated_count}")
        
        # Confirmar cambios
        db.commit()
        
        # Verificar resultados finales
        print("\n📊 RESUMEN FINAL DE ESTADOS:")
        total_tasks = db.query(Task).count()
        pending_tasks = db.query(Task).filter(Task.status == 'pendiente').count()
        in_progress_tasks = db.query(Task).filter(Task.status == 'en_progreso').count()
        completed_tasks = db.query(Task).filter(Task.status == 'completada').count()
        
        print(f"   📋 Total de tareas: {total_tasks}")
        print(f"   ⏳ Pendientes: {pending_tasks}")
        print(f"   🔄 En progreso: {in_progress_tasks}")
        print(f"   ✅ Completadas: {completed_tasks}")
        
        # Estadísticas por empresa
        print(f"\n📊 ESTADÍSTICAS POR EMPRESA:")
        for company in db.query(Company).filter(Company.id.in_([4, 5])).all():
            company_tasks = db.query(Task).filter(Task.company_id == company.id)
            total = company_tasks.count()
            pending = company_tasks.filter(Task.status == 'pendiente').count()
            in_progress = company_tasks.filter(Task.status == 'en_progreso').count()
            completed = company_tasks.filter(Task.status == 'completada').count()
            
            print(f"   🏢 {company.name}:")
            print(f"      Total: {total} | Pendientes: {pending} | En progreso: {in_progress} | Completadas: {completed}")
        
        print("\n🎉 ¡Estados reales actualizados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al actualizar estados: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_real_task_status()

