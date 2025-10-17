#!/usr/bin/env python3
"""
Script para corregir definitivamente los emails de usuarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
import re

def fix_user_emails_final():
    """Corregir definitivamente los emails de usuarios"""
    
    db = SessionLocal()
    
    try:
        print("=== CORRIGIENDO EMAILS DE USUARIOS DEFINITIVAMENTE ===")
        
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
        
        # Primero, limpiar todos los emails para evitar conflictos
        print("1. Limpiando emails existentes...")
        for user in users:
            user.email = f"temp_{user.id}@ko-actuar.com"
        db.commit()
        
        # Ahora asignar emails correctos
        print("2. Asignando emails correctos...")
        used_emails = set()
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
                base_email = f"{simple_username}@ko-actuar.com"
                
                # Verificar si ya existe
                if base_email in used_emails:
                    # Agregar sufijo único
                    counter = 1
                    while True:
                        unique_email = f"{simple_username}_{counter}@ko-actuar.com"
                        if unique_email not in used_emails:
                            base_email = unique_email
                            break
                        counter += 1
                
                used_emails.add(base_email)
                user.email = base_email
                print(f"  ✓ {user.full_name[:40]}... → {base_email}")
                updated_count += 1
            else:
                # Para usuarios que no son asesores (admin, managers, etc.)
                if 'admin' in user.username.lower():
                    user.email = "admin@ko-actuar.com"
                elif 'manager' in user.username.lower():
                    user.email = f"{user.username}@ko-actuar.com"
                else:
                    user.email = f"{user.username}@ko-actuar.com"
                
                used_emails.add(user.email)
                print(f"  ✓ {user.full_name[:40]}... → {user.email}")
                updated_count += 1
        
        db.commit()
        print(f"\n✓ Actualizados {updated_count} emails")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_users = db.query(User).count()
        print(f"Total de usuarios: {total_users}")
        
        # Mostrar algunos usuarios de ejemplo
        print("\n📧 EJEMPLOS DE EMAILS CORREGIDOS:")
        sample_users = db.query(User).filter(User.email.like('%@ko-actuar.com')).limit(20).all()
        for user in sample_users:
            print(f"  • {user.full_name[:50]}... → {user.email}")
        
        # Verificar que no hay duplicados
        print("\n🔍 VERIFICANDO DUPLICADOS:")
        from sqlalchemy import func
        duplicate_emails = db.query(User.email, func.count(User.id)).group_by(User.email).having(func.count(User.id) > 1).all()
        
        if duplicate_emails:
            print("  ❌ Emails duplicados encontrados:")
            for email, count in duplicate_emails:
                print(f"    - {email}: {count} usuarios")
        else:
            print("  ✅ No hay emails duplicados")
        
    except Exception as e:
        print(f"Error durante la corrección: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user_emails_final()
