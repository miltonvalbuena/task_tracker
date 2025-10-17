#!/usr/bin/env python3
"""
Script para simplificar los emails de usuarios a formato: nombre@ko-actuar.com
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
import re

def simplify_user_emails():
    """Simplificar emails de usuarios a formato: nombre@ko-actuar.com"""
    
    db = SessionLocal()
    
    try:
        print("=== SIMPLIFICANDO EMAILS DE USUARIOS ===")
        
        # Obtener todos los usuarios
        users = db.query(User).all()
        
        # Mapeo de nombres de asesores a usernames simples
        asesor_mapping = {
            'Maria José': 'maria_jose',
            'Otoniel': 'otoniel',
            'Gisela': 'gisela',
            'Manuela': 'manuela',
            'Ana': 'ana',
            'Diana': 'diana',
            'Luz': 'luz',
            'Carlos Eduardo': 'carlos_eduardo',
            'Carlos': 'carlos'
        }
        
        updated_count = 0
        
        for user in users:
            # Extraer el nombre del asesor del full_name
            asesor_name = None
            for name, username in asesor_mapping.items():
                if name in user.full_name:
                    asesor_name = name
                    simple_username = username
                    break
            
            if asesor_name:
                # Crear email simple
                new_email = f"{simple_username}@ko-actuar.com"
                
                # Verificar si ya existe otro usuario con este email
                existing_user = db.query(User).filter(User.email == new_email, User.id != user.id).first()
                
                if existing_user:
                    # Si ya existe, agregar un sufijo único
                    counter = 1
                    while True:
                        unique_email = f"{simple_username}_{counter}@ko-actuar.com"
                        existing_check = db.query(User).filter(User.email == unique_email, User.id != user.id).first()
                        if not existing_check:
                            new_email = unique_email
                            break
                        counter += 1
                
                if user.email != new_email:
                    old_email = user.email
                    user.email = new_email
                    print(f"  ✓ {user.full_name}: {old_email} → {new_email}")
                    updated_count += 1
                else:
                    print(f"  - {user.full_name}: {user.email} (ya correcto)")
            else:
                # Para usuarios que no son asesores (admin, managers, etc.)
                if '@ko-actuar.com' not in user.email:
                    # Mantener el username actual pero cambiar dominio
                    username_part = user.email.split('@')[0] if '@' in user.email else user.username
                    new_email = f"{username_part}@ko-actuar.com"
                    
                    if user.email != new_email:
                        old_email = user.email
                        user.email = new_email
                        print(f"  ✓ {user.full_name}: {old_email} → {new_email}")
                        updated_count += 1
                    else:
                        print(f"  - {user.full_name}: {user.email} (ya correcto)")
        
        db.commit()
        print(f"\n✓ Actualizados {updated_count} emails")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_users = db.query(User).count()
        print(f"Total de usuarios: {total_users}")
        
        # Mostrar algunos usuarios de ejemplo
        print("\n📧 EJEMPLOS DE EMAILS SIMPLIFICADOS:")
        sample_users = db.query(User).filter(User.email.like('%@ko-actuar.com')).limit(15).all()
        for user in sample_users:
            print(f"  • {user.full_name[:40]}... → {user.email}")
        
    except Exception as e:
        print(f"Error durante la simplificación: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    simplify_user_emails()
