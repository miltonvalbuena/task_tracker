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
echo "📊 Creando tablas de base de datos..."\n\
cd /app/backend && python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"\n\
echo "✅ Tablas creadas"\n\
echo "📥 Importando datos desde dump SQL..."\n\
python scripts/import_from_dump.py\n\
echo "✅ Datos importados"\n\
echo "🔐 Creando usuario administrador..."\n\
python scripts/init_railway.py\n\
echo "✅ Usuario administrador creado"\n\
echo "🌐 Iniciando servidor..."\n\
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]
