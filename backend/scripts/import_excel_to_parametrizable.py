#!/usr/bin/env python3
"""
Script para importar datos de los archivos Excel al sistema parametrizable
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Client, User, Task, TaskStatus, TaskPriority, UserRole
from app.auth import get_password_hash
from datetime import datetime
import numpy as np

def clean_string(value, max_length=200):
    """Limpiar y truncar strings"""
    if pd.isna(value) or value is None:
        return None
    value = str(value).strip()
    if value == 'nan' or value == 'NaT':
        return None
    if len(value) > max_length:
        value = value[:max_length-3] + "..."
    return value

def clean_date(value):
    """Limpiar fechas"""
    if pd.isna(value) or value is None:
        return None
    if str(value) == 'nan' or str(value) == 'NaT':
        return None
    try:
        if isinstance(value, str):
            # Intentar parsear fechas en formato DD/MM/YYYY
            if '/' in value:
                parts = value.split('/')
                if len(parts) == 3:
                    day, month, year = parts
                    # Corregir años de 2 dígitos
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    return datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
        return pd.to_datetime(value)
    except:
        return None

def create_colmena_client():
    """Crear cliente Colmena ARL con configuración específica"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe
        existing = db.query(Client).filter(Client.name == "COLMENA ARL").first()
        if existing:
            print("✅ Cliente COLMENA ARL ya existe")
            return existing.id
        
        # Crear cliente con configuración específica de Colmena
        client = Client(
            name="COLMENA ARL",
            description="Cliente Colmena ARL - Datos importados desde Excel",
            arl="COLMENA ARL",
            is_active=True,
            custom_fields_config=[
                {
                    "name": "nit",
                    "label": "NIT",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "NIT de la empresa",
                    "help_text": "Número de identificación tributaria"
                },
                {
                    "name": "linea",
                    "label": "Línea",
                    "field_type": "select",
                    "required": False,
                    "options": ["Línea Prevención y Gestión del ATEL", "Línea Acompañamiento Legal y de Gestión"],
                    "help_text": "Línea de trabajo específica"
                },
                {
                    "name": "programa",
                    "label": "Programa",
                    "field_type": "select",
                    "required": False,
                    "options": ["Programa Estilo de Vida Saludable", "Programa Seguridad Vial", "Programa SGSST-ILO", "Programa Construcción Libre de Riesgo", "Sistema Vigilancia Epidemiológica Conservación Respiratoria", "Programa Atenea", "Sistema Vigilancia Epidemiológica Conservación Auditiva"],
                    "help_text": "Programa específico"
                },
                {
                    "name": "componente",
                    "label": "Componente",
                    "field_type": "select",
                    "required": False,
                    "options": ["Formación", "Estandarización", "Entendimiento", "Diagnóstico", "Verificación", "Estandarizacion"],
                    "help_text": "Componente del programa"
                },
                {
                    "name": "actividad",
                    "label": "Actividad",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Tipo de actividad",
                    "help_text": "Tipo de actividad a realizar"
                },
                {
                    "name": "ciudad_desarrollo",
                    "label": "Ciudad de Desarrollo",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Ciudad donde se desarrolla",
                    "help_text": "Ciudad o ubicación donde se realizará la actividad"
                },
                {
                    "name": "detalle_actividad",
                    "label": "Detalle de Actividad",
                    "field_type": "textarea",
                    "required": False,
                    "placeholder": "Detalle específico de la actividad",
                    "help_text": "Descripción detallada de la actividad"
                },
                {
                    "name": "entregables",
                    "label": "Entregables",
                    "field_type": "textarea",
                    "required": False,
                    "placeholder": "Entregables esperados",
                    "help_text": "Lista de entregables esperados"
                },
                {
                    "name": "tipo_actividad",
                    "label": "Tipo de Actividad",
                    "field_type": "select",
                    "required": False,
                    "options": ["Capacitación", "Asesoría"],
                    "help_text": "Tipo de actividad"
                },
                {
                    "name": "nro_os",
                    "label": "Nro. OS",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Número de orden de servicio",
                    "help_text": "Número de orden de servicio"
                },
                {
                    "name": "fecha_final",
                    "label": "Fecha Final",
                    "field_type": "date",
                    "required": False,
                    "help_text": "Fecha final de ejecución"
                },
                {
                    "name": "horas_asignadas",
                    "label": "Horas Asignadas",
                    "field_type": "number",
                    "required": False,
                    "placeholder": "0",
                    "help_text": "Número de horas asignadas"
                },
                {
                    "name": "horas_pendientes",
                    "label": "Horas Pendientes",
                    "field_type": "number",
                    "required": False,
                    "placeholder": "0",
                    "help_text": "Horas pendientes por ejecutar"
                },
                {
                    "name": "dis_responsable",
                    "label": "DIS y/o Responsable ARL",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Nombre del responsable",
                    "help_text": "DIS y/o responsable ARL"
                },
                {
                    "name": "asesor_asignado",
                    "label": "Asesor Asignado",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Nombre del asesor",
                    "help_text": "Asesor asignado"
                },
                {
                    "name": "fecha_asignacion",
                    "label": "Fecha de Asignación",
                    "field_type": "date",
                    "required": False,
                    "help_text": "Fecha de asignación"
                },
                {
                    "name": "observaciones",
                    "label": "Observaciones",
                    "field_type": "textarea",
                    "required": False,
                    "placeholder": "Observaciones adicionales",
                    "help_text": "Observaciones adicionales"
                }
            ]
        )
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        print(f"✅ Cliente COLMENA ARL creado con ID: {client.id}")
        return client.id
        
    except Exception as e:
        print(f"❌ Error al crear cliente Colmena: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def create_positiva_client():
    """Crear cliente Positiva ARL con configuración específica"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe
        existing = db.query(Client).filter(Client.name == "POSITIVA ARL").first()
        if existing:
            print("✅ Cliente POSITIVA ARL ya existe")
            return existing.id
        
        # Crear cliente con configuración específica de Positiva
        client = Client(
            name="POSITIVA ARL",
            description="Cliente Positiva ARL - Datos importados desde Excel",
            arl="POSITIVA ARL",
            is_active=True,
            custom_fields_config=[
                {
                    "name": "nit",
                    "label": "NIT",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "NIT de la empresa",
                    "help_text": "Número de identificación tributaria"
                },
                {
                    "name": "codigo",
                    "label": "Código",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Código de la actividad",
                    "help_text": "Código de la actividad"
                },
                {
                    "name": "actividad",
                    "label": "Actividad",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Tipo de actividad",
                    "help_text": "Tipo de actividad a realizar"
                },
                {
                    "name": "no_aut",
                    "label": "No. Aut",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Número de autorización",
                    "help_text": "Número de autorización"
                },
                {
                    "name": "id_actividad",
                    "label": "Id Actividad",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "ID de la actividad",
                    "help_text": "ID de la actividad"
                },
                {
                    "name": "fecha_autorizacion",
                    "label": "Fecha de Autorización",
                    "field_type": "date",
                    "required": False,
                    "help_text": "Fecha de autorización"
                },
                {
                    "name": "fecha_maxima_ejecucion",
                    "label": "Fecha Máxima de Ejecución",
                    "field_type": "date",
                    "required": False,
                    "help_text": "Fecha máxima de ejecución"
                },
                {
                    "name": "mes",
                    "label": "Mes",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Mes de ejecución",
                    "help_text": "Mes de ejecución"
                },
                {
                    "name": "horas_asignadas",
                    "label": "Horas Asignadas",
                    "field_type": "number",
                    "required": False,
                    "placeholder": "0",
                    "help_text": "Número de horas asignadas"
                },
                {
                    "name": "pendientes_registrar_app",
                    "label": "Pendientes por Registrar desde App",
                    "field_type": "number",
                    "required": False,
                    "placeholder": "0",
                    "help_text": "Pendientes por registrar desde app"
                },
                {
                    "name": "eis",
                    "label": "EIS",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "EIS responsable",
                    "help_text": "EIS responsable"
                },
                {
                    "name": "asesor",
                    "label": "Asesor",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Nombre del asesor",
                    "help_text": "Asesor responsable"
                },
                {
                    "name": "fecha_asignacion",
                    "label": "Fecha de Asignación",
                    "field_type": "date",
                    "required": False,
                    "help_text": "Fecha de asignación"
                },
                {
                    "name": "estado_detallado",
                    "label": "Estado Detallado",
                    "field_type": "select",
                    "required": False,
                    "options": ["Sin Programar", "Programada", "En Progreso", "Completada"],
                    "help_text": "Estado detallado de la actividad"
                },
                {
                    "name": "observaciones",
                    "label": "Observaciones",
                    "field_type": "textarea",
                    "required": False,
                    "placeholder": "Observaciones adicionales",
                    "help_text": "Observaciones adicionales"
                }
            ]
        )
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        print(f"✅ Cliente POSITIVA ARL creado con ID: {client.id}")
        return client.id
        
    except Exception as e:
        print(f"❌ Error al crear cliente Positiva: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def import_colmena_data(file_path, client_id, admin_user_id):
    """Importar datos de Colmena ARL"""
    db = SessionLocal()
    
    try:
        print(f"📊 Importando datos de Colmena ARL...")
        df = pd.read_excel(file_path)
        
        tasks_created = 0
        
        for index, row in df.iterrows():
            # Saltar filas vacías o con datos inválidos
            if pd.isna(row.get('ACTIVIDAD')) or str(row.get('ACTIVIDAD')).strip() in ['nan', 'NaT', '']:
                continue
                
            # Mapear datos de Colmena
            task_data = {
                'title': clean_string(row.get('ACTIVIDAD'), 200),
                'description': clean_string(row.get('DETALLE ACTIVIDAD'), 1000),
                'status': TaskStatus.PENDIENTE,
                'priority': TaskPriority.MEDIA,
                'client_id': client_id,
                'created_by': admin_user_id,
                'custom_fields': {
                    'nit': clean_string(row.get('NIT'), 20),
                    'linea': clean_string(row.get('LINEA'), 100),
                    'programa': clean_string(row.get('PROGRAMA'), 100),
                    'componente': clean_string(row.get('COMPONENTE'), 100),
                    'actividad': clean_string(row.get('ACTIVIDAD'), 200),
                    'ciudad_desarrollo': clean_string(row.get('CIUDAD DE DESARROLLO'), 100),
                    'detalle_actividad': clean_string(row.get('DETALLE ACTIVIDAD'), 2000),
                    'entregables': clean_string(row.get('Entregables'), 1000),
                    'tipo_actividad': clean_string(row.get('Tipo de Actividad'), 50),
                    'nro_os': clean_string(row.get('Nro. OS'), 50),
                    'horas_asignadas': int(row.get('HORAS ASIGNADAS', 0)) if pd.notna(row.get('HORAS ASIGNADAS')) else None,
                    'horas_pendientes': int(row.get('HORAS PENDIENTES POR EJECUTAR', 0)) if pd.notna(row.get('HORAS PENDIENTES POR EJECUTAR')) else None,
                    'dis_responsable': clean_string(row.get('DIS y/o RESPONSABLE ARL'), 100),
                    'asesor_asignado': clean_string(row.get('ASESOR ASIGNADO'), 100),
                    'observaciones': clean_string(row.get('OBSERVACIONES'), 1000),
                }
            }
            
            # Agregar fecha final si existe
            fecha_final = clean_date(row.get('FECHA FINAL'))
            if fecha_final:
                task_data['due_date'] = fecha_final
                task_data['custom_fields']['fecha_final'] = fecha_final.isoformat()
            
            # Agregar fecha de asignación si existe
            fecha_asignacion = clean_date(row.get('FECHA DE ASIGNACIÓN'))
            if fecha_asignacion:
                task_data['custom_fields']['fecha_asignacion'] = fecha_asignacion.isoformat()
            
            # Crear tarea
            task = Task(**task_data)
            db.add(task)
            tasks_created += 1
        
        db.commit()
        print(f"✅ Importadas {tasks_created} tareas de Colmena ARL")
        return tasks_created
        
    except Exception as e:
        print(f"❌ Error al importar datos de Colmena: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def import_positiva_data(file_path, client_id, admin_user_id):
    """Importar datos de Positiva ARL"""
    db = SessionLocal()
    
    try:
        print(f"📊 Importando datos de Positiva ARL...")
        df = pd.read_excel(file_path)
        
        tasks_created = 0
        
        for index, row in df.iterrows():
            # Saltar filas vacías o con datos inválidos
            if pd.isna(row.get('ACTIVIDAD')) or str(row.get('ACTIVIDAD')).strip() in ['nan', 'NaT', '']:
                continue
                
            # Mapear datos de Positiva
            task_data = {
                'title': clean_string(row.get('ACTIVIDAD'), 200),
                'description': f"Empresa: {clean_string(row.get('EMPRESA'), 100)} - Código: {clean_string(row.get('CODIGO'), 50)}",
                'status': TaskStatus.PENDIENTE,
                'priority': TaskPriority.MEDIA,
                'client_id': client_id,
                'created_by': admin_user_id,
                'custom_fields': {
                    'nit': clean_string(row.get('NIT'), 20),
                    'codigo': clean_string(row.get('CODIGO'), 50),
                    'actividad': clean_string(row.get('ACTIVIDAD'), 200),
                    'no_aut': clean_string(row.get('No. Aut'), 50),
                    'id_actividad': clean_string(row.get('Id Actividad'), 50),
                    'mes': clean_string(row.get('MES'), 20),
                    'horas_asignadas': int(row.get('HORAS ASIGNADAS', 0)) if pd.notna(row.get('HORAS ASIGNADAS')) else None,
                    'pendientes_registrar_app': int(row.get('PENDIENTES POR REGISTRAR DESDE APP', 0)) if pd.notna(row.get('PENDIENTES POR REGISTRAR DESDE APP')) else None,
                    'eis': clean_string(row.get('EIS'), 100),
                    'asesor': clean_string(row.get('ASESOR'), 100),
                    'estado_detallado': clean_string(row.get('ESTADO'), 50),
                    'observaciones': clean_string(row.get('OBSERVACIONES'), 1000),
                }
            }
            
            # Agregar fechas si existen
            fecha_autorizacion = clean_date(row.get('FECHA DE AUTORIZACIÓN'))
            if fecha_autorizacion:
                task_data['custom_fields']['fecha_autorizacion'] = fecha_autorizacion.isoformat()
            
            fecha_maxima = clean_date(row.get('FECHA MÁXIMA DE EJECUCIÓN'))
            if fecha_maxima:
                task_data['custom_fields']['fecha_maxima_ejecucion'] = fecha_maxima.isoformat()
                task_data['due_date'] = fecha_maxima
            
            fecha_asignacion = clean_date(row.get('FECHA DE ASIGNACIÓN'))
            if fecha_asignacion:
                task_data['custom_fields']['fecha_asignacion'] = fecha_asignacion.isoformat()
            
            # Crear tarea
            task = Task(**task_data)
            db.add(task)
            tasks_created += 1
        
        db.commit()
        print(f"✅ Importadas {tasks_created} tareas de Positiva ARL")
        return tasks_created
        
    except Exception as e:
        print(f"❌ Error al importar datos de Positiva: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def main():
    print("🚀 Iniciando importación de datos Excel al sistema parametrizable...")
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Obtener usuario admin
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == 'admin').first()
        if not admin_user:
            print("❌ Usuario admin no encontrado")
            return
        admin_user_id = admin_user.id
    finally:
        db.close()
    
    # Crear clientes con configuración específica
    colmena_id = create_colmena_client()
    positiva_id = create_positiva_client()
    
    if not colmena_id or not positiva_id:
        print("❌ Error al crear clientes")
        return
    
    # Importar datos de Colmena
    colmena_file = "/app/Files/Estado de Tareas_COLMENA ARL.xlsx"
    if os.path.exists(colmena_file):
        colmena_tasks = import_colmena_data(colmena_file, colmena_id, admin_user_id)
    else:
        print(f"⚠️ Archivo de Colmena no encontrado: {colmena_file}")
        colmena_tasks = 0
    
    # Importar datos de Positiva
    positiva_file = "/app/Files/Estado de Tareas_POSITIVA ARL.xlsx"
    if os.path.exists(positiva_file):
        positiva_tasks = import_positiva_data(positiva_file, positiva_id, admin_user_id)
    else:
        print(f"⚠️ Archivo de Positiva no encontrado: {positiva_file}")
        positiva_tasks = 0
    
    print(f"\n🎉 Importación completada!")
    print(f"📊 Resumen:")
    print(f"   - Tareas de Colmena ARL: {colmena_tasks}")
    print(f"   - Tareas de Positiva ARL: {positiva_tasks}")
    print(f"   - Total de tareas importadas: {colmena_tasks + positiva_tasks}")
    print(f"\n👤 Credenciales de acceso:")
    print(f"   Usuario: admin")
    print(f"   Contraseña: admin123")
    print(f"\n🌐 URLs:")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Backend API: http://localhost:8000")
    print(f"   Documentación: http://localhost:8000/docs")

if __name__ == "__main__":
    main()


