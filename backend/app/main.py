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

# Incluir routers ANTES del catch-all route
app.include_router(auth.router, prefix="/api/v1")
app.include_router(companies.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

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

# Montar archivos estáticos del frontend DESPUÉS de todos los endpoints de API
frontend_path = "/app/frontend/build"
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=f"{frontend_path}/static"), name="static")
    
    @app.get("/")
    def serve_frontend():
        return FileResponse(f"{frontend_path}/index.html")
    
    # Rutas específicas para el frontend
    @app.get("/dashboard")
    def serve_dashboard():
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/tasks")
    def serve_tasks():
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/users")
    def serve_users():
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/companies")
    def serve_companies():
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/reports")
    def serve_reports():
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/login")
    def serve_login():
        return FileResponse(f"{frontend_path}/index.html")
    
    # No usar catch-all route para evitar interceptar rutas de API
else:
    @app.get("/")
    def read_root():
        return {"message": "Task Tracker API - Sistema de gestión de tareas", "frontend": "Not built"}
