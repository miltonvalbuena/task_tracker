#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de Railway
"""

import os
import sys
import subprocess
import requests
import time

def check_environment_variables():
    """Verificar variables de entorno críticas"""
    print("🔍 Verificando variables de entorno...")
    
    critical_vars = [
        "DATABASE_URL",
        "SECRET_KEY",
        "PORT"
    ]
    
    missing_vars = []
    for var in critical_vars:
        value = os.getenv(var)
        if value:
            if var == "DATABASE_URL":
                # Ocultar credenciales en la URL
                masked_url = value.split("@")[0].split("://")[0] + "://***:***@" + "@".join(value.split("@")[1:])
                print(f"✅ {var}: {masked_url}")
            else:
                print(f"✅ {var}: {'*' * len(value) if 'SECRET' in var else value}")
        else:
            print(f"❌ {var}: No configurada")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_database_connection():
    """Verificar conexión a la base de datos"""
    print("\n🔍 Verificando conexión a la base de datos...")
    
    try:
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Conexión a base de datos exitosa")
                
                # Obtener información adicional
                try:
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"📊 Versión de PostgreSQL: {version}")
                except:
                    pass
                
                return True
            else:
                print("❌ Consulta de prueba falló")
                return False
                
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def check_application_health():
    """Verificar salud de la aplicación"""
    print("\n🔍 Verificando salud de la aplicación...")
    
    port = os.getenv("PORT", "8000")
    health_url = f"http://localhost:{port}/api/v1/health"
    
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Aplicación saludable: {data}")
            return True
        else:
            print(f"❌ Aplicación no saludable: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error verificando salud: {e}")
        return False

def check_railway_status():
    """Verificar estado de Railway (si está disponible)"""
    print("\n🔍 Verificando estado de Railway...")
    
    try:
        # Verificar si Railway CLI está disponible
        result = subprocess.run(["railway", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI disponible")
            print(f"📊 Estado: {result.stdout}")
            return True
        else:
            print("⚠️ Railway CLI no disponible o no autenticado")
            return False
    except FileNotFoundError:
        print("⚠️ Railway CLI no instalado")
        return False
    except Exception as e:
        print(f"❌ Error verificando Railway: {e}")
        return False

def check_network_connectivity():
    """Verificar conectividad de red"""
    print("\n🔍 Verificando conectividad de red...")
    
    # Verificar conectividad básica
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Conectividad de red básica OK")
        else:
            print("⚠️ Conectividad de red limitada")
    except Exception as e:
        print(f"❌ Sin conectividad de red: {e}")
        return False
    
    # Verificar conectividad a Railway
    try:
        response = requests.get("https://railway.app", timeout=5)
        if response.status_code == 200:
            print("✅ Conectividad a Railway OK")
        else:
            print("⚠️ Conectividad a Railway limitada")
    except Exception as e:
        print(f"❌ Sin conectividad a Railway: {e}")
    
    return True

def main():
    """Función principal de diagnóstico"""
    print("🚀 Diagnóstico de Task Tracker en Railway")
    print("=" * 50)
    
    checks = [
        ("Variables de entorno", check_environment_variables),
        ("Conexión a base de datos", check_database_connection),
        ("Salud de la aplicación", check_application_health),
        ("Estado de Railway", check_railway_status),
        ("Conectividad de red", check_network_connectivity)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print("=" * 50)
    
    all_ok = True
    for name, result in results:
        status = "✅ OK" if result else "❌ FALLO"
        print(f"{name}: {status}")
        if not result:
            all_ok = False
    
    print("=" * 50)
    if all_ok:
        print("🎉 Todos los diagnósticos pasaron exitosamente!")
    else:
        print("⚠️ Algunos diagnósticos fallaron. Revisa los errores arriba.")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
