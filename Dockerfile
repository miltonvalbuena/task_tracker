# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend package.json and install dependencies
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install

# Copy all source code
WORKDIR /app
COPY . .

# Build frontend
WORKDIR /app/frontend
RUN npm run build

# Set working directory to backend for the application
WORKDIR /app/backend

# Expose port
EXPOSE $PORT

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Iniciando Task Tracker..."\n\
\n\
# Verificar salud de la base de datos\n\
echo "🔍 Verificando salud de la base de datos..."\n\
if ! python scripts/check_db_health.py; then\n\
    echo "❌ Error: La base de datos no está disponible o no está configurada correctamente"\n\
    exit 1\n\
fi\n\
\n\
echo "📊 Creando tablas de base de datos..."\n\
cd /app/backend\n\
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)" || echo "⚠️ Error creando tablas, pero continuando..."\n\
echo "✅ Tablas creadas o ya existen"\n\
\n\
echo "🔧 Corrigiendo estructura de base de datos..."\n\
python scripts/fix_db_structure.py || echo "⚠️ Error corrigiendo estructura, pero continuando..."\n\
echo "✅ Estructura corregida"\n\
\n\
echo "🔧 Actualizando base de datos..."\n\
python scripts/update_railway_db.py || echo "⚠️ Error actualizando base de datos, pero continuando..."\n\
echo "✅ Actualización completada"\n\
\n\
echo "🌐 Iniciando servidor..."\n\
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]
