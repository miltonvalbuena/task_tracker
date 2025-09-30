#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de Railway
"""

import os
import sys
import subprocess
import time

def test_local_setup():
    """Probar la configuración local"""
    print("🔍 Probando configuración local...")
    
    # Verificar que los archivos necesarios existen
    required_files = [
        "Dockerfile",
        "railway.toml",
        "deploy-railway.sh",
        "backend/scripts/check_db_health.py",
        "backend/scripts/diagnose_railway.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {missing_files}")
        return False
    
    print("✅ Todos los archivos necesarios están presentes")
    return True

def test_railway_cli():
    """Probar Railway CLI"""
    print("\n🔍 Probando Railway CLI...")
    
    try:
        # Verificar si Railway CLI está instalado
        result = subprocess.run(["railway", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Railway CLI instalado: {result.stdout.strip()}")
        else:
            print("❌ Railway CLI no está instalado correctamente")
            return False
        
        # Verificar autenticación
        result = subprocess.run(["railway", "whoami"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Autenticado como: {result.stdout.strip()}")
        else:
            print("⚠️ No autenticado con Railway (esto es normal si no has hecho login)")
        
        return True
        
    except FileNotFoundError:
        print("❌ Railway CLI no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error probando Railway CLI: {e}")
        return False

def test_docker_setup():
    """Probar configuración de Docker"""
    print("\n🔍 Probando configuración de Docker...")
    
    try:
        # Verificar Docker
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker instalado: {result.stdout.strip()}")
        else:
            print("❌ Docker no está instalado")
            return False
        
        # Verificar Docker Compose
        result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose instalado: {result.stdout.strip()}")
        else:
            print("❌ Docker Compose no está instalado")
            return False
        
        return True
        
    except FileNotFoundError:
        print("❌ Docker no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error probando Docker: {e}")
        return False

def test_backend_scripts():
    """Probar scripts del backend"""
    print("\n🔍 Probando scripts del backend...")
    
    try:
        # Cambiar al directorio del backend
        backend_dir = "backend"
        if not os.path.exists(backend_dir):
            print("❌ Directorio backend no encontrado")
            return False
        
        # Probar script de verificación de salud
        script_path = os.path.join(backend_dir, "scripts", "check_db_health.py")
        if os.path.exists(script_path):
            print("✅ Script de verificación de salud encontrado")
        else:
            print("❌ Script de verificación de salud no encontrado")
            return False
        
        # Probar script de diagnóstico
        script_path = os.path.join(backend_dir, "scripts", "diagnose_railway.py")
        if os.path.exists(script_path):
            print("✅ Script de diagnóstico encontrado")
        else:
            print("❌ Script de diagnóstico no encontrado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando scripts del backend: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🚀 Prueba de configuración de Railway para Task Tracker")
    print("=" * 60)
    
    tests = [
        ("Configuración local", test_local_setup),
        ("Railway CLI", test_railway_cli),
        ("Docker", test_docker_setup),
        ("Scripts del backend", test_backend_scripts)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    all_ok = True
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{name}: {status}")
        if not result:
            all_ok = False
    
    print("=" * 60)
    if all_ok:
        print("🎉 Todas las pruebas pasaron! Tu configuración está lista para Railway.")
        print("\n📋 Próximos pasos:")
        print("1. Ejecuta: railway login")
        print("2. Ejecuta: ./deploy-railway.sh")
        print("3. Espera a que el despliegue se complete")
        print("4. Visita tu aplicación en Railway")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\n🔧 Soluciones comunes:")
        print("- Instala Railway CLI: npm install -g @railway/cli")
        print("- Instala Docker: https://docs.docker.com/get-docker/")
        print("- Haz login en Railway: railway login")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
