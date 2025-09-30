#!/usr/bin/env python3
"""
Script para inicializar datos de ejemplo en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Company, User, Task, TaskStatus, TaskPriority, UserRole
from app.auth import get_password_hash
from datetime import datetime, timedelta

def create_sample_data():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos
        if db.query(Company).first():
            print("Los datos de ejemplo ya existen. Saltando inicialización.")
            return
        
        # Crear empresas
        companies = [
            Company(
                name="COLMENA ARL",
                description="Compañía de seguros Colmena ARL",
                is_active=True
            ),
            Company(
                name="POSITIVA ARL",
                description="Compañía de seguros Positiva ARL",
                is_active=True
            ),
            Company(
                name="SURA ARL",
                description="Compañía de seguros Sura ARL",
                is_active=True
            )
        ]
        
        for company in companies:
            db.add(company)
        db.commit()
        
        # Obtener empresas creadas
        colmena = db.query(Company).filter(Company.name == "COLMENA ARL").first()
        positiva = db.query(Company).filter(Company.name == "POSITIVA ARL").first()
        sura = db.query(Company).filter(Company.name == "SURA ARL").first()
        
        # Crear usuarios
        users = [
            # Administradores
            User(
                email="admin@tasktracker.com",
                username="admin",
                full_name="Administrador del Sistema",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                company_id=colmena.id,
                is_active=True
            ),
            
            # Usuarios de Colmena
            User(
                email="manager@colmena.com",
                username="manager_colmena",
                full_name="Manager Colmena",
                hashed_password=get_password_hash("manager123"),
                role=UserRole.MANAGER,
                company_id=colmena.id,
                is_active=True
            ),
            User(
                email="user@colmena.com",
                username="user_colmena",
                full_name="Usuario Colmena",
                hashed_password=get_password_hash("user123"),
                role=UserRole.USER,
                company_id=colmena.id,
                is_active=True
            ),
            
            # Usuarios de Positiva
            User(
                email="manager@positiva.com",
                username="manager_positiva",
                full_name="Manager Positiva",
                hashed_password=get_password_hash("manager123"),
                role=UserRole.MANAGER,
                company_id=positiva.id,
                is_active=True
            ),
            User(
                email="user@positiva.com",
                username="user_positiva",
                full_name="Usuario Positiva",
                hashed_password=get_password_hash("user123"),
                role=UserRole.USER,
                company_id=positiva.id,
                is_active=True
            ),
            
            # Usuarios de Sura
            User(
                email="manager@sura.com",
                username="manager_sura",
                full_name="Manager Sura",
                hashed_password=get_password_hash("manager123"),
                role=UserRole.MANAGER,
                company_id=sura.id,
                is_active=True
            ),
            User(
                email="user@sura.com",
                username="user_sura",
                full_name="Usuario Sura",
                hashed_password=get_password_hash("user123"),
                role=UserRole.USER,
                company_id=sura.id,
                is_active=True
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # Obtener usuarios creados
        admin = db.query(User).filter(User.username == "admin").first()
        manager_colmena = db.query(User).filter(User.username == "manager_colmena").first()
        user_colmena = db.query(User).filter(User.username == "user_colmena").first()
        manager_positiva = db.query(User).filter(User.username == "manager_positiva").first()
        user_positiva = db.query(User).filter(User.username == "user_positiva").first()
        manager_sura = db.query(User).filter(User.username == "manager_sura").first()
        user_sura = db.query(User).filter(User.username == "user_sura").first()
        
        # Crear tareas de ejemplo
        tasks = [
            # Tareas de Colmena
            Task(
                title="Revisar pólizas de seguros",
                description="Revisar y actualizar las pólizas de seguros vigentes",
                status=TaskStatus.PENDIENTE,
                priority=TaskPriority.ALTA,
                due_date=datetime.utcnow() + timedelta(days=7),
                company_id=colmena.id,
                assigned_to=user_colmena.id,
                created_by=manager_colmena.id
            ),
            Task(
                title="Procesar reclamos",
                description="Procesar los reclamos pendientes del mes",
                status=TaskStatus.EN_PROGRESO,
                priority=TaskPriority.CRITICA,
                due_date=datetime.utcnow() + timedelta(days=3),
                company_id=colmena.id,
                assigned_to=user_colmena.id,
                created_by=manager_colmena.id
            ),
            Task(
                title="Actualizar base de datos",
                description="Actualizar la base de datos de clientes",
                status=TaskStatus.COMPLETADA,
                priority=TaskPriority.MEDIA,
                due_date=datetime.utcnow() - timedelta(days=1),
                completed_at=datetime.utcnow() - timedelta(hours=2),
                company_id=colmena.id,
                assigned_to=user_colmena.id,
                created_by=manager_colmena.id
            ),
            
            # Tareas de Positiva
            Task(
                title="Auditoría de procesos",
                description="Realizar auditoría de procesos internos",
                status=TaskStatus.PENDIENTE,
                priority=TaskPriority.ALTA,
                due_date=datetime.utcnow() + timedelta(days=14),
                company_id=positiva.id,
                assigned_to=user_positiva.id,
                created_by=manager_positiva.id
            ),
            Task(
                title="Capacitación del personal",
                description="Organizar capacitación sobre nuevos procedimientos",
                status=TaskStatus.EN_PROGRESO,
                priority=TaskPriority.MEDIA,
                due_date=datetime.utcnow() + timedelta(days=10),
                company_id=positiva.id,
                assigned_to=user_positiva.id,
                created_by=manager_positiva.id
            ),
            
            # Tareas de Sura
            Task(
                title="Implementar nuevo sistema",
                description="Implementar nuevo sistema de gestión",
                status=TaskStatus.PENDIENTE,
                priority=TaskPriority.CRITICA,
                due_date=datetime.utcnow() + timedelta(days=21),
                company_id=sura.id,
                assigned_to=user_sura.id,
                created_by=manager_sura.id
            ),
            Task(
                title="Revisar contratos",
                description="Revisar y renovar contratos de proveedores",
                status=TaskStatus.COMPLETADA,
                priority=TaskPriority.BAJA,
                due_date=datetime.utcnow() - timedelta(days=5),
                completed_at=datetime.utcnow() - timedelta(days=1),
                company_id=sura.id,
                assigned_to=user_sura.id,
                created_by=manager_sura.id
            )
        ]
        
        for task in tasks:
            db.add(task)
        db.commit()
        
        print("✅ Datos de ejemplo creados exitosamente!")
        print("\n📋 Usuarios creados:")
        print("   Admin: admin / admin123")
        print("   Manager Colmena: manager_colmena / manager123")
        print("   Usuario Colmena: user_colmena / user123")
        print("   Manager Positiva: manager_positiva / manager123")
        print("   Usuario Positiva: user_positiva / user123")
        print("   Manager Sura: manager_sura / manager123")
        print("   Usuario Sura: user_sura / user123")
        print(f"\n🏢 Empresas creadas: {len(companies)}")
        print(f"👥 Usuarios creados: {len(users)}")
        print(f"📝 Tareas creadas: {len(tasks)}")
        
    except Exception as e:
        print(f"❌ Error al crear datos de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
