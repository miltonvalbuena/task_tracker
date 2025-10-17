#!/usr/bin/env python3
"""
Script para crear usuarios reales basados en los asesores de los archivos Excel
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

def create_real_users():
    """Crear usuarios reales basados en los asesores de los archivos Excel"""
    
    db = SessionLocal()
    
    try:
        # Obtener ARLs
        colmena_arl = db.query(ARL).filter(ARL.name == "COLMENA ARL").first()
        positiva_arl = db.query(ARL).filter(ARL.name == "POSITIVA ARL").first()
        
        if not colmena_arl or not positiva_arl:
            print("Error: Las ARLs no existen")
            return
        
        # Obtener un cliente por defecto para cada ARL
        colmena_client = db.query(Client).filter(Client.arl_id == colmena_arl.id).first()
        positiva_client = db.query(Client).filter(Client.arl_id == positiva_arl.id).first()
        
        if not colmena_client or not positiva_client:
            print("Error: No hay clientes para las ARLs")
            return
        
        print("=== CREANDO USUARIOS REALES ===")
        
        # Crear usuarios de COLMENA ARL
        print("\n--- Usuarios de COLMENA ARL ---")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            asesores_colmena = df_colmena['ASESOR ASIGNADO'].dropna().unique()
            
            for asesor in asesores_colmena:
                # Crear username del asesor
                username = asesor.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                
                # Verificar si el usuario ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                
                if not existing_user:
                    # Crear usuario
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
                    print(f"  ✓ Creado: {asesor} ({username})")
                else:
                    print(f"  - Ya existe: {asesor} ({username})")
        
        # Crear usuarios de POSITIVA ARL
        print("\n--- Usuarios de POSITIVA ARL ---")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            asesores_positiva = df_positiva['ASESOR'].dropna().unique()
            
            for asesor in asesores_positiva:
                # Crear username del asesor
                username = f"{asesor.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')}_positiva"
                
                # Verificar si el usuario ya existe
                existing_user = db.query(User).filter(User.username == username).first()
                
                if not existing_user:
                    # Crear usuario
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
                    print(f"  ✓ Creado: {asesor} ({username})")
                else:
                    print(f"  - Ya existe: {asesor} ({username})")
        
        db.commit()
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_users = db.query(User).count()
        colmena_users = db.query(User).join(Client).filter(Client.arl_id == colmena_arl.id).count()
        positiva_users = db.query(User).join(Client).filter(Client.arl_id == positiva_arl.id).count()
        
        print(f"Total de usuarios: {total_users}")
        print(f"Usuarios de COLMENA ARL: {colmena_users}")
        print(f"Usuarios de POSITIVA ARL: {positiva_users}")
        
        # Mostrar todos los usuarios creados
        print("\n=== TODOS LOS USUARIOS ===")
        users = db.query(User).all()
        for user in users:
            client_name = user.client.name if user.client else "Sin cliente"
            print(f"• {user.username} - {user.full_name} - {user.role.value} - {client_name[:30]}...")
        
    except Exception as e:
        print(f"Error durante la creación: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_real_users()
