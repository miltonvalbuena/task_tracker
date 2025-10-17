#!/usr/bin/env python3
"""
Script para corregir los nombres de usuarios eliminando el nombre de la empresa
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
import re

def fix_user_names():
    """Corregir los nombres de usuarios eliminando el nombre de la empresa"""
    
    db = SessionLocal()
    
    try:
        print("=== CORRIGIENDO NOMBRES DE USUARIOS ===")
        
        # Obtener todos los usuarios
        users = db.query(User).all()
        
        # Mapeo de nombres de asesores
        asesor_names = [
            'Maria José', 'Otoniel', 'Gisela', 'Manuela', 'Ana', 
            'Diana', 'Luz', 'Carlos Eduardo', 'Carlos'
        ]
        
        updated_count = 0
        
        for user in users:
            original_name = user.full_name
            
            # Si el nombre contiene " - ", extraer solo la parte del asesor
            if ' - ' in user.full_name:
                # Buscar el nombre del asesor al inicio
                for asesor_name in asesor_names:
                    if user.full_name.startswith(asesor_name + ' - '):
                        user.full_name = asesor_name
                        break
                else:
                    # Si no encuentra un patrón conocido, tomar la parte antes del " - "
                    user.full_name = user.full_name.split(' - ')[0]
            elif user.full_name in asesor_names:
                # Ya está correcto
                pass
            else:
                # Para otros usuarios (admin, managers, etc.), mantener el nombre actual
                pass
            
            if user.full_name != original_name:
                print(f"  ✓ {original_name} → {user.full_name}")
                updated_count += 1
            else:
                print(f"  - {user.full_name} (ya correcto)")
        
        db.commit()
        print(f"\n✓ Actualizados {updated_count} nombres")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        total_users = db.query(User).count()
        print(f"Total de usuarios: {total_users}")
        
        # Mostrar algunos usuarios de ejemplo
        print("\n👤 EJEMPLOS DE NOMBRES CORREGIDOS:")
        sample_users = db.query(User).limit(15).all()
        for user in sample_users:
            print(f"  • {user.full_name} ({user.username}) → {user.email}")
        
    except Exception as e:
        print(f"Error durante la corrección: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_user_names()
