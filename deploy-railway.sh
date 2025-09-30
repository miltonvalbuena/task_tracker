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

# Verificar si ya existe un proyecto
if [ ! -f "railway.toml" ]; then
    echo "📦 Inicializando proyecto en Railway..."
    railway init
else
    echo "✅ Proyecto Railway ya configurado"
fi

# Verificar si PostgreSQL está configurado
echo "🗄️ Verificando servicio de PostgreSQL..."
if ! railway variables | grep -q "DATABASE_URL"; then
    echo "📦 Agregando servicio de PostgreSQL..."
    railway add postgresql
    echo "⏳ Esperando a que PostgreSQL esté listo..."
    sleep 10
else
    echo "✅ PostgreSQL ya configurado"
fi

# Configurar variables de entorno
echo "⚙️ Configurando variables de entorno..."
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set ALGORITHM="HS256"
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables set PORT="8000"
railway variables set NODE_ENV="production"
railway variables set ADMIN_USERNAME="admin"
railway variables set ADMIN_EMAIL="admin@ko-actuar.com"
railway variables set ADMIN_PASSWORD="admin123"
railway variables set ADMIN_FULL_NAME="Administrador"

# Obtener el dominio de Railway para CORS
echo "🌐 Obteniendo dominio de Railway..."
RAILWAY_DOMAIN=$(railway domain)
if [ -n "$RAILWAY_DOMAIN" ]; then
    echo "✅ Dominio encontrado: $RAILWAY_DOMAIN"
    railway variables set CORS_ORIGINS="https://$RAILWAY_DOMAIN"
else
    echo "⚠️ No se pudo obtener el dominio, usando placeholder"
    railway variables set CORS_ORIGINS="https://your-project.railway.app"
fi

# Desplegar
echo "🚀 Desplegando aplicación..."
railway up

# Esperar a que el despliegue esté completo
echo "⏳ Esperando a que el despliegue esté completo..."
sleep 30

# Verificar el estado
echo "🔍 Verificando estado del despliegue..."
railway status

# Obtener logs recientes
echo "📝 Mostrando logs recientes..."
railway logs --tail 20

echo ""
echo "✅ Despliegue completado!"
echo "🌐 Tu aplicación estará disponible en: https://$RAILWAY_DOMAIN"
echo "👤 Credenciales de admin: admin / admin123"
echo ""
echo "📊 Comandos útiles:"
echo "   railway status    - Ver estado del proyecto"
echo "   railway logs      - Ver logs en tiempo real"
echo "   railway variables - Ver variables de entorno"
echo "   railway domain    - Ver dominio del proyecto"

