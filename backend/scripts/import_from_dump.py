#!/usr/bin/env python3
"""
Script para importar datos desde el dump SQL a Railway
"""

import os
import sys
import subprocess
from sqlalchemy import create_engine, text

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def import_from_dump():
    """Importar datos desde el dump SQL"""
    print("📥 Importando datos desde dump SQL...")
    
    try:
        # Obtener la URL de la base de datos de Railway
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL no encontrada en variables de entorno")
            return False
        
        # Verificar si el archivo dump existe
        dump_file = "/app/local_database_dump.sql"
        if not os.path.exists(dump_file):
            print(f"❌ Archivo dump no encontrado: {dump_file}")
            return False
        
        # Usar psql para importar el dump
        cmd = [
            "psql",
            database_url,
            "-f", dump_file
        ]
        
        print(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Datos importados exitosamente desde dump SQL")
            return True
        else:
            print(f"❌ Error importando datos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando importación de datos desde dump SQL...")
    
    success = import_from_dump()
    
    if success:
        print("✅ Importación completada exitosamente")
    else:
        print("❌ Importación falló")

if __name__ == "__main__":
    main()
