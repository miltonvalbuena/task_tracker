#!/usr/bin/env python3
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
            4: [  # COLMENA ARL
                "Alejandra Tellez",
                "Ana",
                "Carlos Eduardo",
                "Cesar Mora",
                "Diana",
                "Erika Sosa",
                "Gisela",
                "Julian David Chavarro",
                "Karen Florez",
                "Laura Lorena Romero",
                "Luis Diaz",
                "Luz",
                "Manuela",
                "Maria José",
                "Maria Quijano",
                "María FPrieto",
                "Natalia Aranzazu",
                "Omar David Loaiza",
                "Otoniel",
                "Simon Vanegas",
            ],
        }
        
        created_count = 0
        
        for company_id, user_names in users_data.items():
            print(f"\n🏢 Creando usuarios para empresa ID {company_id}...")
            
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
        print(f"\n🎉 ¡Usuarios creados exitosamente! Total: {created_count}")
        
    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_users()
