#!/usr/bin/env python3
"""
Script para crear usuarios para todos los responsables y asesores de los archivos Excel
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

def create_responsible_users():
    """Crear usuarios para todos los responsables y asesores"""
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Obtener ARLs
        colmena_arl = db.query(ARL).filter(ARL.name == "COLMENA ARL").first()
        positiva_arl = db.query(ARL).filter(ARL.name == "POSITIVA ARL").first()
        
        if not colmena_arl or not positiva_arl:
            print("Error: Las ARLs no existen. Ejecuta primero init_data.py")
            return
        
        # Obtener un cliente de cada ARL para asignar a los usuarios
        colmena_client = db.query(Client).filter(Client.arl_id == colmena_arl.id).first()
        positiva_client = db.query(Client).filter(Client.arl_id == positiva_arl.id).first()
        
        if not colmena_client or not positiva_client:
            print("Error: No hay clientes en las ARLs")
            return
        
        print(f"Cliente COLMENA: {colmena_client.name}")
        print(f"Cliente POSITIVA: {positiva_client.name}")
        
        # Crear usuarios para responsables de COLMENA ARL
        print("\n=== CREANDO USUARIOS PARA RESPONSABLES DE COLMENA ARL ===")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            
            # Responsables ARL
            responsables_arl = df_colmena['DIS y/o RESPONSABLE ARL'].dropna().unique()
            print(f"Creando usuarios para {len(responsables_arl)} responsables ARL...")
            
            for responsable in responsables_arl:
                # Crear username único
                username = responsable.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                email = f"{username}@colmena.com"
                
                # Verificar si el usuario ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    print(f"  - Ya existe: {responsable}")
                    continue
                
                # Crear usuario
                user = User(
                    email=email,
                    username=username,
                    full_name=responsable,
                    hashed_password=get_password_hash("password123"),
                    role=UserRole.MANAGER,
                    client_id=colmena_client.id,
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Creado: {responsable} ({username})")
            
            # Asesores asignados
            asesores = df_colmena['ASESOR ASIGNADO'].dropna().unique()
            print(f"\nCreando usuarios para {len(asesores)} asesores...")
            
            for asesor in asesores:
                # Crear username único
                username = asesor.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                email = f"{username}@colmena.com"
                
                # Verificar si el usuario ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    print(f"  - Ya existe: {asesor}")
                    continue
                
                # Crear usuario
                user = User(
                    email=email,
                    username=username,
                    full_name=asesor,
                    hashed_password=get_password_hash("password123"),
                    role=UserRole.USER,
                    client_id=colmena_client.id,
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Creado: {asesor} ({username})")
            
            db.commit()
            print(f"✓ Usuarios de COLMENA ARL creados")
        
        # Crear usuarios para responsables de POSITIVA ARL
        print("\n=== CREANDO USUARIOS PARA RESPONSABLES DE POSITIVA ARL ===")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            
            # Responsables EIS
            eis_responsables = df_positiva['EIS'].dropna().unique()
            print(f"Creando usuarios para {len(eis_responsables)} responsables EIS...")
            
            for responsable in eis_responsables:
                # Crear username único
                username = f"{responsable.lower()}_positiva"
                email = f"{responsable.lower()}@positiva.com"
                
                # Verificar si el usuario ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    print(f"  - Ya existe: {responsable}")
                    continue
                
                # Crear usuario
                user = User(
                    email=email,
                    username=username,
                    full_name=responsable,
                    hashed_password=get_password_hash("password123"),
                    role=UserRole.MANAGER,
                    client_id=positiva_client.id,
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Creado: {responsable} ({username})")
            
            # Asesores
            asesores = df_positiva['ASESOR'].dropna().unique()
            print(f"\nCreando usuarios para {len(asesores)} asesores...")
            
            for asesor in asesores:
                # Crear username único
                username = f"{asesor.lower().replace(' ', '_')}_positiva"
                email = f"{asesor.lower().replace(' ', '_')}@positiva.com"
                
                # Verificar si el usuario ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    print(f"  - Ya existe: {asesor}")
                    continue
                
                # Crear usuario
                user = User(
                    email=email,
                    username=username,
                    full_name=asesor,
                    hashed_password=get_password_hash("password123"),
                    role=UserRole.USER,
                    client_id=positiva_client.id,
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Creado: {asesor} ({username})")
            
            db.commit()
            print(f"✓ Usuarios de POSITIVA ARL creados")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_users = db.query(User).count()
        admin_users = db.query(User).filter(User.role == UserRole.ADMIN).count()
        manager_users = db.query(User).filter(User.role == UserRole.MANAGER).count()
        regular_users = db.query(User).filter(User.role == UserRole.USER).count()
        
        print(f"Total de usuarios en la base de datos: {total_users}")
        print(f"Administradores: {admin_users}")
        print(f"Managers: {manager_users}")
        print(f"Usuarios regulares: {regular_users}")
        
        # Mostrar usuarios por ARL
        colmena_users = db.query(User).join(Client).filter(Client.arl_id == colmena_arl.id).count()
        positiva_users = db.query(User).join(Client).filter(Client.arl_id == positiva_arl.id).count()
        
        print(f"Usuarios de COLMENA ARL: {colmena_users}")
        print(f"Usuarios de POSITIVA ARL: {positiva_users}")
        
    except Exception as e:
        print(f"Error durante la creación de usuarios: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_responsible_users()
