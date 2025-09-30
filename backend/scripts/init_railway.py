#!/usr/bin/env python3
"""
Script de inicialización para Railway
Crea el usuario administrador y configura la base de datos
"""

import os
import sys
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Agregar el directorio padre al path para importar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, User, Company
from app.database import get_db

# Configuración de contraseñas
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def create_admin_user():
    """Crear usuario administrador"""
    print("🔐 Creando usuario administrador...")
    
    # Obtener configuración desde variables de entorno
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@ko-actuar.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_full_name = os.getenv("ADMIN_FULL_NAME", "Administrador")
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar si el usuario admin ya existe
        existing_admin = db.query(User).filter(User.username == admin_username).first()
        
        if existing_admin:
            print(f"✅ Usuario administrador '{admin_username}' ya existe")
            return
        
        # Crear hash de la contraseña
        hashed_password = pwd_context.hash(admin_password)
        
        # Crear usuario administrador
        admin_user = User(
            username=admin_username,
            email=admin_email,
            full_name=admin_full_name,
            hashed_password=hashed_password,
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print(f"✅ Usuario administrador creado exitosamente:")
        print(f"   Usuario: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Contraseña: {admin_password}")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        db.rollback()
    finally:
        db.close()

def create_default_company():
    """Crear empresa por defecto"""
    print("🏢 Creando empresa por defecto...")
    
    db = next(get_db())
    
    try:
        # Verificar si ya existe una empresa por defecto
        existing_company = db.query(Company).filter(Company.name == "EMPRESA PRINCIPAL").first()
        
        if existing_company:
            print("✅ Empresa por defecto ya existe")
            return
        
        # Crear empresa por defecto
        default_company = Company(
            name="EMPRESA PRINCIPAL",
            description="Empresa principal del sistema - completamente configurable",
            is_active=True,
            custom_fields_config=[
                {
                    "name": "nit",
                    "label": "NIT",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Ingrese el NIT de la empresa",
                    "help_text": "Número de identificación tributaria"
                },
                {
                    "name": "programa",
                    "label": "Programa",
                    "field_type": "select",
                    "required": False,
                    "options": [
                        "Programa Estilo de Vida Saludable",
                        "Programa Seguridad Vial",
                        "Programa SGSST-ILO"
                    ],
                    "help_text": "Seleccione el programa correspondiente"
                },
                {
                    "name": "componente",
                    "label": "Componente",
                    "field_type": "select",
                    "required": False,
                    "options": [
                        "Formación",
                        "Estandarización",
                        "Diagnóstico",
                        "Verificación"
                    ],
                    "help_text": "Componente del programa"
                },
                {
                    "name": "tipo_actividad",
                    "label": "Tipo de Actividad",
                    "field_type": "select",
                    "required": False,
                    "options": [
                        "Capacitación",
                        "Asesoría",
                        "Diagnóstico",
                        "Verificación"
                    ],
                    "help_text": "Tipo de actividad a realizar"
                },
                {
                    "name": "ciudad_desarrollo",
                    "label": "Ciudad de Desarrollo",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Ciudad donde se desarrolla la actividad",
                    "help_text": "Ciudad o ubicación donde se realizará la actividad"
                },
                {
                    "name": "horas_asignadas",
                    "label": "Horas Asignadas",
                    "field_type": "number",
                    "required": False,
                    "placeholder": "0",
                    "help_text": "Número de horas asignadas para la actividad"
                },
                {
                    "name": "fecha_final",
                    "label": "Fecha Final",
                    "field_type": "date",
                    "required": False,
                    "help_text": "Fecha límite para completar la actividad"
                },
                {
                    "name": "responsable",
                    "label": "Responsable",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Nombre del responsable",
                    "help_text": "Persona responsable de la actividad"
                },
                {
                    "name": "observaciones",
                    "label": "Observaciones",
                    "field_type": "textarea",
                    "required": False,
                    "placeholder": "Observaciones adicionales...",
                    "help_text": "Cualquier observación o comentario adicional"
                }
            ]
        )
        
        db.add(default_company)
        db.commit()
        
        print("✅ Empresa por defecto creada exitosamente")
        
    except Exception as e:
        print(f"❌ Error al crear empresa por defecto: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 Inicializando Task Tracker para Railway...")
    
    try:
        # Crear usuario administrador
        create_admin_user()
        
        # Crear empresa por defecto
        create_default_company()
        
        print("✅ Inicialización completada exitosamente")
        print("🌐 La aplicación está lista para usar")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

