#!/usr/bin/env python3
"""
Script para limpiar tareas existentes y volver a importar todas las actividades
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Task

def clean_and_reimport():
    """Limpiar tareas existentes y volver a importar"""
    
    db = SessionLocal()
    
    try:
        # Contar tareas existentes
        existing_tasks = db.query(Task).count()
        print(f"Tareas existentes: {existing_tasks}")
        
        # Eliminar todas las tareas existentes
        print("Eliminando tareas existentes...")
        db.query(Task).delete()
        db.commit()
        print("✓ Tareas eliminadas")
        
        # Ejecutar el script de importación
        print("\nEjecutando script de importación...")
        from scripts.import_activities_from_excel import import_activities_from_excel
        import_activities_from_excel()
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_and_reimport()
