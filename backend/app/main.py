import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def read_root():
    return {"message": "Task Tracker API - Sistema de gestión de tareas"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "service": "Task Tracker API"}

@app.get("/health")
def health_check_alt():
    return {"status": "healthy", "service": "Task Tracker API"}
