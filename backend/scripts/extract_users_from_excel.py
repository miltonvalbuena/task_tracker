#!/usr/bin/env python3
"""
Script para extraer usuarios únicos de los archivos Excel
y crear un script de importación de usuarios
"""

import pandas as pd
import os
from collections import defaultdict

def extract_users_from_excel():
    """Extrae usuarios únicos de los archivos Excel"""
    
    # Rutas de los archivos Excel
    excel_files = [
        "Files/Estado de Tareas_COLMENA ARL.xlsx",
        "Files/Estado de Tareas_POSITIVA ARL.xlsx"
    ]
    
    # Diccionario para almacenar usuarios por empresa
    users_by_company = defaultdict(set)
    
    # Mapeo de nombres de archivos a IDs de empresa
    company_mapping = {
        "COLMENA ARL": 4,  # ID de COLMENA ARL en la base de datos
        "POSITIVA ARL": 5  # ID de POSITIVA ARL en la base de datos
    }
    
    for excel_file in excel_files:
        if not os.path.exists(excel_file):
            print(f"⚠️  Archivo no encontrado: {excel_file}")
            continue
            
        print(f"📊 Analizando: {excel_file}")
        
        try:
            # Leer el archivo Excel
            df = pd.read_excel(excel_file)
            
            # Mostrar las columnas disponibles
            print(f"   Columnas disponibles: {list(df.columns)}")
            
            # Buscar columnas que puedan contener nombres de usuarios
            user_columns = []
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['responsable', 'asignado', 'usuario', 'nombre', 'ejecutor']):
                    user_columns.append(col)
            
            print(f"   Columnas de usuario encontradas: {user_columns}")
            
            # Extraer usuarios únicos de cada columna
            for col in user_columns:
                # Obtener valores únicos no nulos
                unique_users = df[col].dropna().unique()
                
                # Filtrar valores que parezcan nombres de personas
                for user in unique_users:
                    user_str = str(user).strip()
                    if user_str and len(user_str) > 2 and not user_str.lower() in ['nan', 'none', 'null', '']:
                        # Determinar la empresa basada en el nombre del archivo
                        company_name = None
                        for company_key in company_mapping.keys():
                            if company_key in excel_file:
                                company_name = company_key
                                break
                        
                        if company_name:
                            users_by_company[company_name].add(user_str)
            
            print(f"   Usuarios encontrados: {len(users_by_company.get(company_name, set()))}")
            
        except Exception as e:
            print(f"❌ Error al procesar {excel_file}: {e}")
    
    # Mostrar resumen
    print("\n" + "="*50)
    print("📋 RESUMEN DE USUARIOS ENCONTRADOS")
    print("="*50)
    
    total_users = 0
    for company_name, users in users_by_company.items():
        print(f"\n🏢 {company_name} (ID: {company_mapping[company_name]}):")
        for user in sorted(users):
            print(f"   - {user}")
        total_users += len(users)
        print(f"   Total: {len(users)} usuarios")
    
    print(f"\n📊 TOTAL DE USUARIOS ÚNICOS: {total_users}")
    
    return users_by_company, company_mapping

def generate_user_creation_script(users_by_company, company_mapping):
    """Genera un script para crear usuarios en la base de datos"""
    
    script_content = '''#!/usr/bin/env python3
"""
Script generado automáticamente para crear usuarios extraídos de Excel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Company, UserRole
from app.auth import get_password_hash
import random
import string

def generate_username(full_name):
    """Genera un username basado en el nombre completo"""
    # Tomar las primeras letras de cada palabra
    words = full_name.lower().split()
    if len(words) >= 2:
        username = words[0][:3] + words[1][:3]
    else:
        username = words[0][:6]
    
    # Agregar números aleatorios si es necesario
    username += str(random.randint(10, 99))
    return username

def generate_email(full_name, company_name):
    """Genera un email basado en el nombre y empresa"""
    username = generate_username(full_name)
    company_domain = company_name.lower().replace(' ', '').replace('arl', '') + '.com'
    return f"{username}@{company_domain}"

def create_users():
    """Crea todos los usuarios extraídos de Excel"""
    
    db = SessionLocal()
    
    try:
        # Datos de usuarios por empresa
        users_data = {
'''
    
    # Agregar datos de usuarios
    for company_name, users in users_by_company.items():
        company_id = company_mapping[company_name]
        script_content += f"            {company_id}: [  # {company_name}\n"
        for user in sorted(users):
            script_content += f'                "{user}",\n'
        script_content += "            ],\n"
    
    script_content += '''        }
        
        created_count = 0
        
        for company_id, user_names in users_data.items():
            print(f"\\n🏢 Creando usuarios para empresa ID {company_id}...")
            
            for full_name in user_names:
                # Generar username único
                username = generate_username(full_name)
                counter = 1
                original_username = username
                
                # Verificar que el username sea único
                while db.query(User).filter(User.username == username).first():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                # Generar email
                email = generate_email(full_name, f"empresa_{company_id}")
                counter = 1
                original_email = email
                
                # Verificar que el email sea único
                while db.query(User).filter(User.email == email).first():
                    email = f"{original_email.split('@')[0]}{counter}@{original_email.split('@')[1]}"
                    counter += 1
                
                # Crear usuario
                user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    hashed_password=get_password_hash("password123"),  # Contraseña por defecto
                    role=UserRole.USER,
                    company_id=company_id,
                    is_active=True
                )
                
                db.add(user)
                created_count += 1
                print(f"   ✅ {full_name} -> {username} ({email})")
        
        db.commit()
        print(f"\\n🎉 ¡Usuarios creados exitosamente! Total: {created_count}")
        
    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_users()
'''
    
    # Escribir el script
    script_path = "/app/scripts/create_users_from_excel.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n📝 Script generado: {script_path}")
    return script_path

if __name__ == "__main__":
    print("🔍 Extrayendo usuarios de archivos Excel...")
    users_by_company, company_mapping = extract_users_from_excel()
    
    if users_by_company:
        print("\n📝 Generando script de creación de usuarios...")
        script_path = generate_user_creation_script(users_by_company, company_mapping)
        print(f"\n✅ Proceso completado. Ejecuta: python {script_path}")
    else:
        print("\n❌ No se encontraron usuarios en los archivos Excel")
