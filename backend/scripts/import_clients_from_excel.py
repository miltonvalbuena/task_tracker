#!/usr/bin/env python3
"""
Script para importar todos los clientes de los archivos Excel a la base de datos
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

def import_clients_from_excel():
    """Importar clientes desde archivos Excel"""
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existen ARLs
        colmena_arl = db.query(ARL).filter(ARL.name == "COLMENA ARL").first()
        positiva_arl = db.query(ARL).filter(ARL.name == "POSITIVA ARL").first()
        
        if not colmena_arl or not positiva_arl:
            print("Error: Las ARLs no existen. Ejecuta primero init_data.py")
            return
        
        print(f"ARL COLMENA encontrada: {colmena_arl.id}")
        print(f"ARL POSITIVA encontrada: {positiva_arl.id}")
        
        # Importar clientes de COLMENA ARL
        print("\n=== IMPORTANDO CLIENTES DE COLMENA ARL ===")
        colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
        if os.path.exists(colmena_file):
            df_colmena = pd.read_excel(colmena_file)
            
            # Obtener empresas únicas
            empresas_colmena = df_colmena['EMPRESA'].dropna().unique()
            print(f"Encontradas {len(empresas_colmena)} empresas en COLMENA ARL")
            
            for empresa in empresas_colmena:
                # Verificar si el cliente ya existe
                existing_client = db.query(Client).filter(
                    Client.name == empresa,
                    Client.arl_id == colmena_arl.id
                ).first()
                
                if not existing_client:
                    # Obtener NIT si está disponible
                    nit = None
                    empresa_data = df_colmena[df_colmena['EMPRESA'] == empresa]
                    if not empresa_data.empty and 'NIT' in empresa_data.columns:
                        nit_value = empresa_data['NIT'].iloc[0]
                        if pd.notna(nit_value):
                            nit = str(nit_value)
                    
                    # Crear cliente
                    client = Client(
                        name=empresa,
                        nit=nit,
                        description=f"Cliente de {colmena_arl.name}",
                        arl_id=colmena_arl.id,
                        is_active=True
                    )
                    db.add(client)
                    print(f"  ✓ Creado: {empresa}")
                else:
                    print(f"  - Ya existe: {empresa}")
            
            db.commit()
            print(f"✓ Importados {len(empresas_colmena)} clientes de COLMENA ARL")
        else:
            print(f"❌ Archivo no encontrado: {colmena_file}")
        
        # Importar clientes de POSITIVA ARL
        print("\n=== IMPORTANDO CLIENTES DE POSITIVA ARL ===")
        positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
        if os.path.exists(positiva_file):
            df_positiva = pd.read_excel(positiva_file)
            
            # Obtener empresas únicas
            empresas_positiva = df_positiva['EMPRESA'].dropna().unique()
            print(f"Encontradas {len(empresas_positiva)} empresas en POSITIVA ARL")
            
            for empresa in empresas_positiva:
                # Verificar si el cliente ya existe
                existing_client = db.query(Client).filter(
                    Client.name == empresa,
                    Client.arl_id == positiva_arl.id
                ).first()
                
                if not existing_client:
                    # Obtener NIT si está disponible
                    nit = None
                    empresa_data = df_positiva[df_positiva['EMPRESA'] == empresa]
                    if not empresa_data.empty and 'NIT' in empresa_data.columns:
                        nit_value = empresa_data['NIT'].iloc[0]
                        if pd.notna(nit_value):
                            nit = str(nit_value)
                    
                    # Crear cliente
                    client = Client(
                        name=empresa,
                        nit=nit,
                        description=f"Cliente de {positiva_arl.name}",
                        arl_id=positiva_arl.id,
                        is_active=True
                    )
                    db.add(client)
                    print(f"  ✓ Creado: {empresa}")
                else:
                    print(f"  - Ya existe: {empresa}")
            
            db.commit()
            print(f"✓ Importados {len(empresas_positiva)} clientes de POSITIVA ARL")
        else:
            print(f"❌ Archivo no encontrado: {positiva_file}")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_clients = db.query(Client).count()
        colmena_clients = db.query(Client).filter(Client.arl_id == colmena_arl.id).count()
        positiva_clients = db.query(Client).filter(Client.arl_id == positiva_arl.id).count()
        
        print(f"Total de clientes en la base de datos: {total_clients}")
        print(f"Clientes de COLMENA ARL: {colmena_clients}")
        print(f"Clientes de POSITIVA ARL: {positiva_clients}")
        
    except Exception as e:
        print(f"Error durante la importación: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_clients_from_excel()
