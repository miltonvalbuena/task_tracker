import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import auth, companies, users, tasks, dashboard

app = FastAPI(
    title="Task Tracker API",
    description="Sistema de gestión de tareas para múltiples empresas",
    version="1.0.0"
)

# Configurar CORS para Railway
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(companies.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

# Montar archivos estáticos del frontend
frontend_path = "/app/frontend/build"
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=f"{frontend_path}/static"), name="static")
    
    @app.get("/")
    def serve_frontend():
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/{path:path}")
    def serve_frontend_routes(path: str):
        # Si es una ruta de API, no servir el frontend
        if path.startswith("api/"):
            return {"error": "API endpoint not found"}
        
        # Para todas las demás rutas, servir el index.html del frontend
        return FileResponse(f"{frontend_path}/index.html")
else:
    @app.get("/")
    def read_root():
        return {"message": "Task Tracker API - Sistema de gestión de tareas", "frontend": "Not built"}

@app.get("/api/v1/health")
def health_check():
    """Endpoint de salud que verifica la conexión a la base de datos"""
    try:
        from app.database import engine
        from sqlalchemy import text
        
        # Verificar conexión a la base de datos
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy", 
            "service": "Task Tracker API",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "service": "Task Tracker API",
            "database": "disconnected",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }

@app.get("/health")
def health_check_alt():
    """Endpoint de salud alternativo"""
    return health_check()
