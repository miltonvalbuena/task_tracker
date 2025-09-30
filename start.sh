#!/bin/bash

echo "🚀 Iniciando Task Tracker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Crear directorio de datos de PostgreSQL si no existe
mkdir -p postgres_data

# Construir y ejecutar contenedores
echo "📦 Construyendo contenedores..."
docker-compose up --build -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10

# Verificar que los servicios estén ejecutándose
echo "🔍 Verificando servicios..."
docker-compose ps

echo ""
echo "✅ Task Tracker iniciado exitosamente!"
echo ""
echo "🌐 Aplicaciones disponibles:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Documentación API: http://localhost:8000/docs"
echo ""
echo "👤 Credenciales de prueba:"
echo "   Admin: admin / admin123"
echo "   Usuario: user_colmena / user123"
echo ""
echo "📋 Para detener los servicios:"
echo "   docker-compose down"
echo ""
echo "📊 Para ver logs:"
echo "   docker-compose logs -f"
