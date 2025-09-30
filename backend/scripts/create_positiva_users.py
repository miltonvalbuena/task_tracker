#!/usr/bin/env python3
"""
Script para crear usuarios de POSITIVA ARL extraídos de Excel
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

def create_positiva_users():
    """Crea usuarios de POSITIVA ARL extraídos de Excel"""
    
    db = SessionLocal()
    
    try:
        # Usuarios de POSITIVA ARL (ID: 5)
        positiva_users = [
            "Ana",
            "Carlos", 
            "Luz",
            "Maria José",
            "Otoniel"
        ]
        
        company_id = 5  # POSITIVA ARL
        created_count = 0
        
        print(f"🏢 Creando usuarios para POSITIVA ARL (ID: {company_id})...")
        
        for full_name in positiva_users:
            # Generar username único
            username = generate_username(full_name)
            counter = 1
            original_username = username
            
            # Verificar que el username sea único
            while db.query(User).filter(User.username == username).first():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Generar email
            email = generate_email(full_name, "positiva")
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
        print(f"\n🎉 ¡Usuarios de POSITIVA ARL creados exitosamente! Total: {created_count}")
        
    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_positiva_users()

