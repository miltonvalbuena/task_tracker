#!/usr/bin/env python3
"""
Script para inicializar el sistema parametrizable
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Company, User, UserRole
import hashlib

def hash_password(password: str) -> str:
    """Hash simple de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_system():
    """Inicializar el sistema parametrizable"""
    db = SessionLocal()
    
    try:
        print("🚀 Inicializando sistema parametrizable...")
        
        # Crear empresa principal (puede ser cualquier nombre)
        main_company = Company(
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
                    "options": ["Programa Estilo de Vida Saludable", "Programa Seguridad Vial", "Programa SGSST-ILO"],
                    "help_text": "Seleccione el programa correspondiente"
                },
                {
                    "name": "componente",
                    "label": "Componente",
                    "field_type": "select",
                    "required": False,
                    "options": ["Formación", "Estandarización", "Diagnóstico", "Verificación"],
                    "help_text": "Componente del programa"
                },
                {
                    "name": "tipo_actividad",
                    "label": "Tipo de Actividad",
                    "field_type": "select",
                    "required": False,
                    "options": ["Capacitación", "Asesoría", "Diagnóstico", "Verificación"],
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
        
        # Verificar si ya existe
        existing_company = db.query(Company).filter(Company.name == main_company.name).first()
        if not existing_company:
            db.add(main_company)
            db.commit()
            print(f"✅ Empresa principal creada: {main_company.name}")
        else:
            main_company = existing_company
            print(f"✅ Empresa principal ya existe: {main_company.name}")
        
        # Crear usuario administrador principal
        admin_user = User(
            email="admin@tasktracker.com",
            username="admin",
            full_name="Administrador del Sistema",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
            company_id=main_company.id,
            is_active=True
        )
        
        # Verificar si ya existe
        existing_admin = db.query(User).filter(User.username == admin_user.username).first()
        if not existing_admin:
            db.add(admin_user)
            db.commit()
            print(f"✅ Administrador principal creado: {admin_user.username}")
        else:
            print(f"✅ Administrador principal ya existe: {admin_user.username}")
        
        print(f"\n🎉 Sistema parametrizable inicializado exitosamente!")
        print(f"📊 Empresa principal: {main_company.name}")
        print(f"👤 Administrador: {admin_user.username}")
        print(f"🔧 Campos personalizados configurados: {len(main_company.custom_fields_config)}")
        
        print(f"\n🌐 URLs de acceso:")
        print(f"   Frontend: http://localhost:3000")
        print(f"   Backend API: http://localhost:8000")
        print(f"   Documentación API: http://localhost:8000/docs")
        
        print(f"\n👤 Credenciales de acceso:")
        print(f"   Usuario: admin")
        print(f"   Contraseña: admin123")
        
        print(f"\n📋 Campos personalizados disponibles:")
        for field in main_company.custom_fields_config:
            print(f"   - {field['label']} ({field['field_type']})")
        
        return main_company.id, admin_user.id
        
    except Exception as e:
        print(f"❌ Error al inicializar el sistema: {e}")
        db.rollback()
        return None, None
    finally:
        db.close()

def create_example_companies():
    """Crear empresas de ejemplo con configuraciones diferentes"""
    db = SessionLocal()
    
    try:
        print(f"\n🏢 Creando empresas de ejemplo...")
        
        # Empresa de ejemplo 1: ARL
        arl_company = Company(
            name="ARL EJEMPLO",
            description="Empresa ARL de ejemplo con campos específicos",
            is_active=True,
            custom_fields_config=[
                {
                    "name": "nit",
                    "label": "NIT",
                    "field_type": "text",
                    "required": True,
                    "placeholder": "NIT de la empresa",
                    "help_text": "Número de identificación tributaria"
                },
                {
                    "name": "linea",
                    "label": "Línea de Trabajo",
                    "field_type": "select",
                    "required": True,
                    "options": ["Línea Prevención y Gestión del ATEL", "Línea Acompañamiento Legal y de Gestión"],
                    "help_text": "Línea de trabajo específica"
                },
                {
                    "name": "programa",
                    "label": "Programa",
                    "field_type": "select",
                    "required": True,
                    "options": ["Programa Estilo de Vida Saludable", "Programa Seguridad Vial", "Programa SGSST-ILO"],
                    "help_text": "Programa específico"
                },
                {
                    "name": "tipo_actividad",
                    "label": "Tipo de Actividad",
                    "field_type": "select",
                    "required": True,
                    "options": ["Capacitación", "Asesoría"],
                    "help_text": "Tipo de actividad"
                },
                {
                    "name": "horas_asignadas",
                    "label": "Horas Asignadas",
                    "field_type": "number",
                    "required": True,
                    "placeholder": "0",
                    "help_text": "Horas asignadas"
                },
                {
                    "name": "asesor_asignado",
                    "label": "Asesor Asignado",
                    "field_type": "text",
                    "required": False,
                    "placeholder": "Nombre del asesor",
                    "help_text": "Asesor responsable"
                }
            ]
        )
        
        # Empresa de ejemplo 2: Constructora
        constructora_company = Company(
            name="CONSTRUCTORA EJEMPLO",
            description="Empresa constructora de ejemplo",
            is_active=True,
            custom_fields_config=[
                {
                    "name": "proyecto",
                    "label": "Proyecto",
                    "field_type": "text",
                    "required": True,
                    "placeholder": "Nombre del proyecto",
                    "help_text": "Nombre del proyecto de construcción"
                },
                {
                    "name": "ubicacion",
                    "label": "Ubicación",
                    "field_type": "text",
                    "required": True,
                    "placeholder": "Ciudad, dirección",
                    "help_text": "Ubicación del proyecto"
                },
                {
                    "name": "tipo_trabajo",
                    "label": "Tipo de Trabajo",
                    "field_type": "select",
                    "required": True,
                    "options": ["Excavación", "Estructura", "Acabados", "Instalaciones"],
                    "help_text": "Tipo de trabajo a realizar"
                },
                {
                    "name": "presupuesto",
                    "label": "Presupuesto",
                    "field_type": "number",
                    "required": False,
                    "placeholder": "0",
                    "help_text": "Presupuesto asignado"
                },
                {
                    "name": "fecha_inicio",
                    "label": "Fecha de Inicio",
                    "field_type": "date",
                    "required": True,
                    "help_text": "Fecha de inicio del trabajo"
                },
                {
                    "name": "supervisor",
                    "label": "Supervisor",
                    "field_type": "text",
                    "required": True,
                    "placeholder": "Nombre del supervisor",
                    "help_text": "Supervisor responsable"
                }
            ]
        )
        
        # Verificar si ya existen
        existing_arl = db.query(Company).filter(Company.name == arl_company.name).first()
        if not existing_arl:
            db.add(arl_company)
            print(f"✅ Empresa ARL creada: {arl_company.name}")
        else:
            print(f"✅ Empresa ARL ya existe: {arl_company.name}")
        
        existing_constructora = db.query(Company).filter(Company.name == constructora_company.name).first()
        if not existing_constructora:
            db.add(constructora_company)
            print(f"✅ Empresa Constructora creada: {constructora_company.name}")
        else:
            print(f"✅ Empresa Constructora ya existe: {constructora_company.name}")
        
        db.commit()
        
        print(f"\n📊 Empresas de ejemplo creadas:")
        print(f"   - ARL EJEMPLO: {len(arl_company.custom_fields_config)} campos personalizados")
        print(f"   - CONSTRUCTORA EJEMPLO: {len(constructora_company.custom_fields_config)} campos personalizados")
        
    except Exception as e:
        print(f"❌ Error al crear empresas de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("🚀 Inicializando sistema de gestión de tareas parametrizable...")
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    
    # Inicializar sistema principal
    company_id, admin_id = init_system()
    
    if company_id and admin_id:
        # Crear empresas de ejemplo
        create_example_companies()
        
        print(f"\n🎉 ¡Sistema completamente parametrizable listo!")
        print(f"\n💡 Características del sistema:")
        print(f"   ✅ Multi-empresa con aislamiento de datos")
        print(f"   ✅ Campos personalizables por empresa")
        print(f"   ✅ Configuración dinámica sin hardcodeo")
        print(f"   ✅ Escalable para cualquier tipo de empresa")
        print(f"   ✅ Un solo administrador para todo el sistema")
        
        print(f"\n🔧 Para agregar nuevas empresas:")
        print(f"   1. Acceder como administrador")
        print(f"   2. Ir a 'Empresas' en el menú")
        print(f"   3. Crear nueva empresa")
        print(f"   4. Configurar campos personalizados")
        print(f"   5. Crear usuarios para la empresa")
        
    else:
        print("❌ Error al inicializar el sistema")

if __name__ == "__main__":
    main()
