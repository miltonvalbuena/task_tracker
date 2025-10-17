#!/usr/bin/env python3
"""
Script simple para limpiar usuarios genéricos en Railway
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal

def clean_railway_users():
    """Eliminar usuarios genéricos del sistema usando SQL directo"""
    db = SessionLocal()
    try:
        print("🧹 Limpiando usuarios genéricos en Railway...")
        
        # Lista de usuarios genéricos a eliminar
        generic_usernames = [
            'manager_colmena',
            'usuario_colmena', 
            'manager_positiva',
            'usuario_positiva',
            'manager_sura',
            'usuario_sura'
        ]
        
        # Verificar cuáles existen
        for username in generic_usernames:
            result = db.execute(text("SELECT id, username, full_name FROM users WHERE username = :username"), 
                              {"username": username}).fetchone()
            if result:
                user_id, username, full_name = result
                print(f"📋 Encontrado: {username} ({full_name}) - ID: {user_id}")
                
                # Verificar si tiene tareas asignadas
                task_count = db.execute(text("SELECT COUNT(*) FROM tasks WHERE assigned_to = :user_id"), 
                                      {"user_id": user_id}).scalar()
                
                if task_count > 0:
                    print(f"⚠️  Usuario {username} tiene {task_count} tareas asignadas")
                    # Reasignar tareas al admin
                    admin_result = db.execute(text("SELECT id FROM users WHERE username = 'admin'")).fetchone()
                    if admin_result:
                        admin_id = admin_result[0]
                        db.execute(text("UPDATE tasks SET assigned_to = :admin_id WHERE assigned_to = :user_id"), 
                                 {"admin_id": admin_id, "user_id": user_id})
                        print(f"   ✅ {task_count} tareas reasignadas al admin")
                
                # Eliminar el usuario
                db.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": user_id})
                print(f"   🗑️  Usuario {username} eliminado")
            else:
                print(f"✅ Usuario {username} no encontrado")
        
        db.commit()
        print("✅ Limpieza de usuarios genéricos completada")
        
        # Mostrar estadísticas finales
        total_users = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        print(f"📊 Total de usuarios restantes: {total_users}")
        
    except Exception as e:
        print(f"❌ Error limpiando usuarios genéricos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_railway_users()
