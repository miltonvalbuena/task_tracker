#!/bin/bash

echo "🚀 Desplegando Task Tracker en Railway..."

# Verificar que Railway CLI esté instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado. Instalando..."
    npm install -g @railway/cli
fi

# Verificar autenticación
echo "🔐 Verificando autenticación con Railway..."
if ! railway whoami &> /dev/null; then
    echo "❌ No estás autenticado. Por favor ejecuta: railway login"
    echo "Esto abrirá tu navegador para autenticarte."
    exit 1
fi

# Crear nuevo proyecto en Railway
echo "📦 Creando proyecto en Railway..."
railway init

# Agregar servicio de PostgreSQL
echo "🗄️ Agregando servicio de PostgreSQL..."
railway add postgresql

# Configurar variables de entorno
echo "⚙️ Configurando variables de entorno..."
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set ALGORITHM="HS256"
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables set BACKEND_PORT="8000"
railway variables set BACKEND_HOST="0.0.0.0"
railway variables set NODE_ENV="production"
railway variables set ADMIN_USERNAME="admin"
railway variables set ADMIN_EMAIL="admin@ko-actuar.com"
railway variables set ADMIN_PASSWORD="admin123"
railway variables set ADMIN_FULL_NAME="Administrador"
railway variables set CORS_ORIGINS="https://your-project.railway.app"

# Desplegar
echo "🚀 Desplegando aplicación..."
railway up

echo "✅ Despliegue completado!"
echo "🌐 Tu aplicación estará disponible en tu dominio de Railway"
echo "👤 Credenciales de admin: admin / admin123"
echo "📊 Para ver el estado: railway status"
echo "📝 Para ver logs: railway logs"

