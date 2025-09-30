#!/usr/bin/env python3
"""
Script para importar datos desde la base de datos local a Railway
"""

import os
import sys
import asyncio
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, User, Company, Task
from app.database import get_db

def get_local_db_connection():
    """Conectar a la base de datos local"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="task_tracker",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a base de datos local: {e}")
        return None

def get_railway_db_connection():
    """Conectar a la base de datos de Railway"""
    try:
        # Usar la URL de Railway desde variables de entorno
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL no encontrada en variables de entorno")
            return None
        
        engine = create_engine(database_url)
        return engine
    except Exception as e:
        print(f"❌ Error conectando a base de datos de Railway: {e}")
        return None

def import_companies(local_conn, railway_engine):
    """Importar empresas"""
    print("🏢 Importando empresas...")
    
    try:
        # Obtener empresas de la base local
        local_cursor = local_conn.cursor()
        local_cursor.execute("SELECT * FROM companies")
        companies_data = local_cursor.fetchall()
        
        # Obtener columnas
        columns = [desc[0] for desc in local_cursor.description]
        
        # Crear sesión de Railway
        Session = sessionmaker(bind=railway_engine)
        session = Session()
        
        imported_count = 0
        for row in companies_data:
            company_dict = dict(zip(columns, row))
            
            # Verificar si ya existe
            existing = session.query(Company).filter(Company.name == company_dict['name']).first()
            if not existing:
                company = Company(
                    name=company_dict['name'],
                    description=company_dict.get('description', ''),
                    is_active=company_dict.get('is_active', True),
                    custom_fields_config=company_dict.get('custom_fields_config', [])
                )
                session.add(company)
                imported_count += 1
        
        session.commit()
        session.close()
        print(f"✅ {imported_count} empresas importadas")
        
    except Exception as e:
        print(f"❌ Error importando empresas: {e}")

def import_users(local_conn, railway_engine):
    """Importar usuarios"""
    print("👥 Importando usuarios...")
    
    try:
        # Obtener usuarios de la base local
        local_cursor = local_conn.cursor()
        local_cursor.execute("SELECT * FROM users")
        users_data = local_cursor.fetchall()
        
        # Obtener columnas
        columns = [desc[0] for desc in local_cursor.description]
        
        # Crear sesión de Railway
        Session = sessionmaker(bind=railway_engine)
        session = Session()
        
        imported_count = 0
        for row in users_data:
            user_dict = dict(zip(columns, row))
            
            # Verificar si ya existe
            existing = session.query(User).filter(User.username == user_dict['username']).first()
            if not existing:
                user = User(
                    username=user_dict['username'],
                    email=user_dict['email'],
                    full_name=user_dict.get('full_name', ''),
                    hashed_password=user_dict['hashed_password'],
                    role=user_dict.get('role', 'user'),
                    is_active=user_dict.get('is_active', True),
                    company_id=user_dict.get('company_id')
                )
                session.add(user)
                imported_count += 1
        
        session.commit()
        session.close()
        print(f"✅ {imported_count} usuarios importados")
        
    except Exception as e:
        print(f"❌ Error importando usuarios: {e}")

def import_tasks(local_conn, railway_engine):
    """Importar tareas"""
    print("📋 Importando tareas...")
    
    try:
        # Obtener tareas de la base local
        local_cursor = local_conn.cursor()
        local_cursor.execute("SELECT * FROM tasks")
        tasks_data = local_cursor.fetchall()
        
        # Obtener columnas
        columns = [desc[0] for desc in local_cursor.description]
        
        # Crear sesión de Railway
        Session = sessionmaker(bind=railway_engine)
        session = Session()
        
        imported_count = 0
        for row in tasks_data:
            task_dict = dict(zip(columns, row))
            
            # Verificar si ya existe
            existing = session.query(Task).filter(Task.id == task_dict['id']).first()
            if not existing:
                task = Task(
                    id=task_dict['id'],
                    title=task_dict['title'],
                    description=task_dict.get('description', ''),
                    status=task_dict.get('status', 'pending'),
                    priority=task_dict.get('priority', 'medium'),
                    company_id=task_dict.get('company_id'),
                    assigned_to=task_dict.get('assigned_to'),
                    created_by=task_dict.get('created_by'),
                    due_date=task_dict.get('due_date'),
                    custom_fields=task_dict.get('custom_fields', {}),
                    excel_row_number=task_dict.get('excel_row_number'),
                    excel_sheet_name=task_dict.get('excel_sheet_name')
                )
                session.add(task)
                imported_count += 1
        
        session.commit()
        session.close()
        print(f"✅ {imported_count} tareas importadas")
        
    except Exception as e:
        print(f"❌ Error importando tareas: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando importación de datos desde base local...")
    
    # Conectar a base de datos local
    local_conn = get_local_db_connection()
    if not local_conn:
        print("❌ No se pudo conectar a la base de datos local")
        return
    
    # Conectar a base de datos de Railway
    railway_engine = get_railway_db_connection()
    if not railway_engine:
        print("❌ No se pudo conectar a la base de datos de Railway")
        return
    
    try:
        # Importar datos
        import_companies(local_conn, railway_engine)
        import_users(local_conn, railway_engine)
        import_tasks(local_conn, railway_engine)
        
        print("✅ Importación completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
    finally:
        local_conn.close()

if __name__ == "__main__":
    main()
