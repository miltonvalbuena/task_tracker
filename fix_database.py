#!/usr/bin/env python3
"""
Script para solucionar problemas de base de datos en Railway
"""

import subprocess
import time

def fix_database_connection():
    """Solucionar conexión a la base de datos"""
    print("🔧 Solucionando conexión a la base de datos...")
    
    # 1. Verificar variables de entorno
    print("1️⃣ Verificando variables de entorno...")
    result = subprocess.run(['railway', 'variables', '--service', 'task-tracker-app'], 
                          capture_output=True, text=True)
    print(result.stdout)
    
    # 2. Probar conexión directa a la base de datos
    print("2️⃣ Probando conexión directa...")
    result = subprocess.run(['railway', 'run', 'psql', '$DATABASE_URL', '-c', 'SELECT 1;'], 
                          capture_output=True, text=True)
    print("Resultado de la conexión:")
    print(result.stdout)
    if result.stderr:
        print("Errores:")
        print(result.stderr)
    
    # 3. Crear usuario administrador directamente
    print("3️⃣ Creando usuario administrador...")
    create_user_script = '''
import os
import sys
sys.path.append('/app/backend')
from app.database import engine
from app.models import User
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    db = SessionLocal()
    
    # Verificar si el usuario admin ya existe
    existing_admin = db.query(User).filter(User.username == "admin").first()
    
    if existing_admin:
        print("✅ Usuario admin ya existe")
        print(f"ID: {existing_admin.id}")
        print(f"Email: {existing_admin.email}")
        print(f"Activo: {existing_admin.is_active}")
    else:
        # Crear usuario administrador
        hashed_password = pwd_context.hash("admin123")
        admin_user = User(
            username="admin",
            email="admin@ko-actuar.com",
            full_name="Administrador",
            hashed_password=hashed_password,
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Usuario administrador creado exitosamente")
        print(f"ID: {admin_user.id}")
    
    db.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Escribir script temporal
    with open('/tmp/create_user.py', 'w') as f:
        f.write(create_user_script)
    
    # Ejecutar script
    result = subprocess.run(['railway', 'run', 'python', '/tmp/create_user.py'], 
                          capture_output=True, text=True, timeout=60)
    print("Resultado de crear usuario:")
    print(result.stdout)
    if result.stderr:
        print("Errores:")
        print(result.stderr)
    
    return result.returncode == 0

def main():
    """Función principal"""
    print("🚀 Solucionando problemas de base de datos en Railway...")
    
    success = fix_database_connection()
    
    if success:
        print("✅ Problemas solucionados")
    else:
        print("❌ Algunos problemas persisten")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
