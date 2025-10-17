#!/usr/bin/env python3
"""
Script para cambiar todos los dominios de email a @ko-actuar.com con emails únicos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User

def fix_user_domains_unique():
    """Cambiar todos los dominios de email a @ko-actuar.com con emails únicos"""
    
    db = SessionLocal()
    
    try:
        # Obtener todos los usuarios
        users = db.query(User).all()
        
        print("=== CAMBIANDO DOMINIOS A @ko-actuar.com (ÚNICOS) ===")
        
        used_emails = set()
        
        for user in users:
            # Generar email único basado en el username
            base_email = f"{user.username}@ko-actuar.com"
            
            # Si el email ya existe, agregar un sufijo
            email = base_email
            counter = 1
            while email in used_emails:
                email = f"{user.username}_{counter}@ko-actuar.com"
                counter += 1
            
            used_emails.add(email)
            
            if user.email != email:
                old_email = user.email
                user.email = email
                print(f"  ✓ {user.full_name}: {old_email} → {email}")
            else:
                print(f"  - {user.full_name}: {user.email} (ya correcto)")
        
        db.commit()
        print("✓ Dominios actualizados exitosamente")
        
        # Mostrar resumen
        print("\n=== RESUMEN ===")
        total_users = db.query(User).count()
        print(f"Total de usuarios: {total_users}")
        
        # Mostrar algunos usuarios de ejemplo
        print("\nUsuarios actualizados:")
        sample_users = db.query(User).limit(10).all()
        for user in sample_users:
            print(f"  - {user.full_name}: {user.email}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user_domains_unique()
