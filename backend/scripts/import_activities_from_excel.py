#!/usr/bin/env python3
"""
Script para importar todas las actividades de los archivos Excel como tareas en la base de datos
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
import re

def parse_date(date_str):
    """Parsear fecha desde string"""
    if pd.isna(date_str) or date_str == '':
        return None
    
    try:
        # Intentar diferentes formatos de fecha
        if isinstance(date_str, str):
            # Formato DD/MM/YYYY
            if '/' in date_str:
                return datetime.strptime(date_str, '%d/%m/%Y')
            # Formato YYYY-MM-DD
            elif '-' in date_str:
                return datetime.strptime(date_str, '%Y-%m-%d')
        elif isinstance(date_str, datetime):
            return date_str
        elif hasattr(date_str, 'date'):
            return date_str.date()
    except:
        pass
    
    return None

def determine_task_status(estado_str, fecha_final):
    """Determinar el estado de la tarea basado en el estado y fecha"""
    if pd.isna(estado_str):
        estado_str = ""
    
    estado_str = str(estado_str).lower()
    
    if 'completada' in estado_str or 'finalizada' in estado_str or 'terminada' in estado_str:
        return TaskStatus.COMPLETADA
    elif 'en progreso' in estado_str or 'en proceso' in estado_str or 'ejecutando' in estado_str:
        return TaskStatus.EN_PROGRESO
    elif 'cancelada' in estado_str or 'anulada' in estado_str:
        return TaskStatus.CANCELADA
    else:
        # Si no hay estado específico, determinar por fecha
        if fecha_final:
            if fecha_final < datetime.now():
                return TaskStatus.PENDIENTE  # Vencida pero pendiente
            else:
                return TaskStatus.PENDIENTE
        return TaskStatus.PENDIENTE

def determine_task_priority(horas_asignadas, observaciones):
    """Determinar la prioridad de la tarea"""
    if pd.isna(horas_asignadas):
        horas_asignadas = 0
    
    try:
        horas = float(horas_asignadas)
        if horas >= 100:
            return TaskPriority.CRITICA
        elif horas >= 50:
            return TaskPriority.ALTA
        elif horas >= 20:
            return TaskPriority.MEDIA
        else:
            return TaskPriority.BAJA
    except:
        return TaskPriority.MEDIA

def import_activities_from_excel():
    """Importar actividades desde archivos Excel"""
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Obtener ARLs y usuarios admin
        colmena_arl = db.query(ARL).filter(ARL.name == "COLMENA ARL").first()
        positiva_arl = db.query(ARL).filter(ARL.name == "POSITIVA ARL").first()
        
        # Obtener usuario admin para crear las tareas
        admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
        
        if not colmena_arl or not positiva_arl or not admin_user:
            print("Error: ARLs o usuario admin no existen. Ejecuta primero init_data.py")
            return
        
        print(f"Usuario admin encontrado: {admin_user.username}")
        
        # Importar actividades de COLMENA ARL
        print("\n=== IMPORTANDO ACTIVIDADES DE COLMENA ARL ===")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            
            print(f"Procesando {len(df_colmena)} actividades de COLMENA ARL...")
            
            for index, row in df_colmena.iterrows():
                try:
                    # Obtener cliente
                    empresa = row['EMPRESA']
                    if pd.isna(empresa):
                        continue
                        
                    client = db.query(Client).filter(
                        Client.name == empresa,
                        Client.arl_id == colmena_arl.id
                    ).first()
                    
                    if not client:
                        print(f"  ⚠ Cliente no encontrado: {empresa}")
                        continue
                    
                    # Verificar si la tarea ya existe
                    actividad = row['ACTIVIDAD']
                    if pd.isna(actividad):
                        continue
                    
                    existing_task = db.query(Task).filter(
                        Task.title == actividad,
                        Task.client_id == client.id
                    ).first()
                    
                    if existing_task:
                        continue  # Ya existe
                    
                    # Crear tarea
                    fecha_final = parse_date(row.get('FECHA FINAL'))
                    horas_asignadas = row.get('HORAS ASIGNADAS', 0)
                    observaciones = row.get('OBSERVACIONES', '')
                    
                    # Crear descripción detallada
                    descripcion_parts = []
                    if not pd.isna(row.get('DETALLE ACTIVIDAD')):
                        descripcion_parts.append(f"Detalle: {row['DETALLE ACTIVIDAD']}")
                    if not pd.isna(row.get('Entregables')):
                        descripcion_parts.append(f"Entregables: {row['Entregables']}")
                    if not pd.isna(row.get('Tipo de Actividad')):
                        descripcion_parts.append(f"Tipo: {row['Tipo de Actividad']}")
                    if not pd.isna(row.get('CIUDAD DE DESARROLLO')):
                        descripcion_parts.append(f"Ciudad: {row['CIUDAD DE DESARROLLO']}")
                    if not pd.isna(observaciones):
                        descripcion_parts.append(f"Observaciones: {observaciones}")
                    
                    descripcion = "\n".join(descripcion_parts) if descripcion_parts else "Actividad importada desde Excel"
                    
                    # Campos personalizados
                    custom_fields = {}
                    if not pd.isna(row.get('NIT')):
                        custom_fields['nit'] = str(row['NIT'])
                    if not pd.isna(row.get('LINEA')):
                        custom_fields['linea'] = str(row['LINEA'])
                    if not pd.isna(row.get('PROGRAMA')):
                        custom_fields['programa'] = str(row['PROGRAMA'])
                    if not pd.isna(row.get('COMPONENTE')):
                        custom_fields['componente'] = str(row['COMPONENTE'])
                    if not pd.isna(row.get('Nro. OS')):
                        custom_fields['numero_os'] = str(row['Nro. OS'])
                    if not pd.isna(row.get('ASESOR ASIGNADO')):
                        custom_fields['asesor_asignado'] = str(row['ASESOR ASIGNADO'])
                    if not pd.isna(row.get('HORAS PENDIENTES POR EJECUTAR')):
                        custom_fields['horas_pendientes'] = str(row['HORAS PENDIENTES POR EJECUTAR'])
                    
                    # Truncar título si es muy largo
                    title = actividad[:200] if len(actividad) > 200 else actividad
                    
                    task = Task(
                        title=title,
                        description=descripcion,
                        status=TaskStatus.PENDIENTE,
                        priority=determine_task_priority(horas_asignadas, observaciones),
                        due_date=fecha_final,
                        client_id=client.id,
                        created_by=admin_user.id,
                        custom_fields=custom_fields
                    )
                    
                    db.add(task)
                    
                    if (index + 1) % 10 == 0:
                        print(f"  Procesadas {index + 1}/{len(df_colmena)} actividades...")
                        
                except Exception as e:
                    print(f"  ❌ Error procesando fila {index}: {e}")
                    continue
            
            db.commit()
            print(f"✓ Importadas actividades de COLMENA ARL")
        else:
            print(f"❌ Archivo no encontrado: {colmena_file}")
        
        # Importar actividades de POSITIVA ARL
        print("\n=== IMPORTANDO ACTIVIDADES DE POSITIVA ARL ===")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            
            print(f"Procesando {len(df_positiva)} actividades de POSITIVA ARL...")
            
            for index, row in df_positiva.iterrows():
                try:
                    # Obtener cliente
                    empresa = row['EMPRESA']
                    if pd.isna(empresa):
                        continue
                        
                    client = db.query(Client).filter(
                        Client.name == empresa,
                        Client.arl_id == positiva_arl.id
                    ).first()
                    
                    if not client:
                        print(f"  ⚠ Cliente no encontrado: {empresa}")
                        continue
                    
                    # Verificar si la tarea ya existe
                    actividad = row['ACTIVIDAD']
                    if pd.isna(actividad):
                        continue
                    
                    existing_task = db.query(Task).filter(
                        Task.title == actividad,
                        Task.client_id == client.id
                    ).first()
                    
                    if existing_task:
                        continue  # Ya existe
                    
                    # Crear tarea
                    fecha_maxima = parse_date(row.get('FECHA MÁXIMA DE EJECUCIÓN'))
                    horas_asignadas = row.get('HORAS ASIGNADAS', 0)
                    observaciones = row.get('OBSERVACIONES', '')
                    estado = row.get('ESTADO', '')
                    
                    # Crear descripción detallada
                    descripcion_parts = []
                    if not pd.isna(row.get('CODIGO')):
                        descripcion_parts.append(f"Código: {row['CODIGO']}")
                    if not pd.isna(row.get('No. Aut')):
                        descripcion_parts.append(f"No. Autorización: {row['No. Aut']}")
                    if not pd.isna(row.get('Id Actividad')):
                        descripcion_parts.append(f"ID Actividad: {row['Id Actividad']}")
                    if not pd.isna(row.get('MES')):
                        descripcion_parts.append(f"Mes: {row['MES']}")
                    if not pd.isna(row.get('EIS')):
                        descripcion_parts.append(f"EIS: {row['EIS']}")
                    if not pd.isna(row.get('ASESOR')):
                        descripcion_parts.append(f"Asesor: {row['ASESOR']}")
                    if not pd.isna(observaciones):
                        descripcion_parts.append(f"Observaciones: {observaciones}")
                    
                    descripcion = "\n".join(descripcion_parts) if descripcion_parts else "Actividad importada desde Excel"
                    
                    # Campos personalizados
                    custom_fields = {}
                    if not pd.isna(row.get('NIT')):
                        custom_fields['nit'] = str(row['NIT'])
                    if not pd.isna(row.get('CODIGO')):
                        custom_fields['codigo'] = str(row['CODIGO'])
                    if not pd.isna(row.get('No. Aut')):
                        custom_fields['numero_autorizacion'] = str(row['No. Aut'])
                    if not pd.isna(row.get('Id Actividad')):
                        custom_fields['id_actividad'] = str(row['Id Actividad'])
                    if not pd.isna(row.get('ASESOR')):
                        custom_fields['asesor'] = str(row['ASESOR'])
                    if not pd.isna(row.get('PENDIENTES POR REGISTRAR DESDE APP')):
                        custom_fields['pendientes_app'] = str(row['PENDIENTES POR REGISTRAR DESDE APP'])
                    
                    # Truncar título si es muy largo
                    title = actividad[:200] if len(actividad) > 200 else actividad
                    
                    task = Task(
                        title=title,
                        description=descripcion,
                        status=determine_task_status(estado, fecha_maxima),
                        priority=determine_task_priority(horas_asignadas, observaciones),
                        due_date=fecha_maxima,
                        client_id=client.id,
                        created_by=admin_user.id,
                        custom_fields=custom_fields
                    )
                    
                    db.add(task)
                    
                    if (index + 1) % 100 == 0:
                        print(f"  Procesadas {index + 1}/{len(df_positiva)} actividades...")
                        
                except Exception as e:
                    print(f"  ❌ Error procesando fila {index}: {e}")
                    continue
            
            db.commit()
            print(f"✓ Importadas actividades de POSITIVA ARL")
        else:
            print(f"❌ Archivo no encontrado: {positiva_file}")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_tasks = db.query(Task).count()
        colmena_tasks = db.query(Task).join(Client).filter(Client.arl_id == colmena_arl.id).count()
        positiva_tasks = db.query(Task).join(Client).filter(Client.arl_id == positiva_arl.id).count()
        
        print(f"Total de tareas en la base de datos: {total_tasks}")
        print(f"Tareas de COLMENA ARL: {colmena_tasks}")
        print(f"Tareas de POSITIVA ARL: {positiva_tasks}")
        
        # Mostrar estadísticas por estado
        print("\n=== ESTADÍSTICAS POR ESTADO ===")
        for status in TaskStatus:
            count = db.query(Task).filter(Task.status == status).count()
            print(f"{status.value}: {count}")
        
    except Exception as e:
        print(f"Error durante la importación: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_activities_from_excel()
