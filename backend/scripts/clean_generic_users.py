#!/usr/bin/env python3
"""
Script para eliminar usuarios genéricos de Railway
Elimina: Manager Colmena, Usuario Colmena, Manager Positiva, Usuario Positiva, Manager Sura, Usuario Sura
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Task

def clean_generic_users():
    """Eliminar usuarios genéricos del sistema"""
    db = SessionLocal()
    try:
        print("🧹 Limpiando usuarios genéricos...")
        
        # Lista de usuarios genéricos a eliminar
        generic_usernames = [
            'manager_colmena',
            'usuario_colmena', 
            'manager_positiva',
            'usuario_positiva',
            'manager_sura',
            'usuario_sura'
        ]
        
        # Buscar usuarios genéricos
        generic_users = db.query(User).filter(User.username.in_(generic_usernames)).all()
        
        if not generic_users:
            print("✅ No se encontraron usuarios genéricos para eliminar")
            return
        
        print(f"📋 Usuarios genéricos encontrados: {len(generic_users)}")
        for user in generic_users:
            print(f"   - {user.username} ({user.full_name})")
        
        # Verificar si tienen tareas asignadas
        for user in generic_users:
            assigned_tasks = db.query(Task).filter(Task.assigned_to == user.id).count()
            if assigned_tasks > 0:
                print(f"⚠️  Usuario {user.username} tiene {assigned_tasks} tareas asignadas")
                # Reasignar tareas al admin
                admin_user = db.query(User).filter(User.username == 'admin').first()
                if admin_user:
                    # Solo actualizar assigned_to
                    db.query(Task).filter(Task.assigned_to == user.id).update({
                        Task.assigned_to: admin_user.id
                    })
                    print(f"   ✅ Tareas reasignadas al admin")
        
        # Eliminar usuarios genéricos
        deleted_count = 0
        for user in generic_users:
            db.delete(user)
            deleted_count += 1
            print(f"   🗑️  Eliminado: {user.username}")
        
        db.commit()
        print(f"✅ {deleted_count} usuarios genéricos eliminados exitosamente")
        
        # Mostrar estadísticas finales
        total_users = db.query(User).count()
        print(f"📊 Total de usuarios restantes: {total_users}")
        
    except Exception as e:
        print(f"❌ Error eliminando usuarios genéricos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_generic_users()
