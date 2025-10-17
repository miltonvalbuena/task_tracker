#!/usr/bin/env python3
"""
Script para cambiar todos los dominios de email a @ko-actuar.com
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User

def fix_user_domains():
    """Cambiar todos los dominios de email a @ko-actuar.com"""
    
    db = SessionLocal()
    
    try:
        # Obtener todos los usuarios
        users = db.query(User).all()
        
        print("=== CAMBIANDO DOMINIOS A @ko-actuar.com ===")
        
        for user in users:
            # Cambiar el dominio del email
            if '@' in user.email:
                username_part = user.email.split('@')[0]
                new_email = f"{username_part}@ko-actuar.com"
                
                if user.email != new_email:
                    old_email = user.email
                    user.email = new_email
                    print(f"  ✓ {user.full_name}: {old_email} → {new_email}")
                else:
                    print(f"  - {user.full_name}: {user.email} (ya correcto)")
            else:
                print(f"  ⚠ Email inválido: {user.email}")
        
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
    fix_user_domains()
