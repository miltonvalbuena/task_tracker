#!/usr/bin/env python3
"""
Script para corregir emails inválidos en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User

def fix_invalid_emails():
    """Corregir emails inválidos en la base de datos"""
    
    db = SessionLocal()
    
    try:
        # Buscar usuarios con emails inválidos
        users = db.query(User).all()
        
        print("=== CORRIGIENDO EMAILS INVÁLIDOS ===")
        
        for user in users:
            # Verificar si el email contiene espacios
            if ' ' in user.email:
                old_email = user.email
                # Corregir el email
                user.email = user.email.replace(' ', '_')
                print(f"  ✓ Corregido: {old_email} → {user.email}")
        
        db.commit()
        print("✓ Emails corregidos exitosamente")
        
        # Mostrar resumen
        print("\n=== RESUMEN ===")
        total_users = db.query(User).count()
        print(f"Total de usuarios: {total_users}")
        
        # Mostrar algunos usuarios de ejemplo
        print("\nUsuarios de POSITIVA ARL:")
        positiva_users = db.query(User).filter(User.email.like('%@positiva.com')).limit(5).all()
        for user in positiva_users:
            print(f"  - {user.full_name}: {user.email}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_invalid_emails()
