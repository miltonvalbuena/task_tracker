# Task Tracker - Sistema de Gestión de Tareas

Sistema completo de gestión de tareas para múltiples empresas, desarrollado con FastAPI (Python) y React.

## Características

- **Multi-empresa**: Soporte para múltiples empresas con aislamiento de datos
- **Gestión de usuarios**: Sistema de roles (Admin, Manager, Usuario)
- **Gestión de tareas**: Creación, edición, asignación y seguimiento de tareas
- **Dashboard interactivo**: Estadísticas y gráficos en tiempo real
- **Sistema de reportes**: Exportación de datos y análisis detallados
- **Autenticación segura**: JWT tokens con roles y permisos
- **Base de datos PostgreSQL**: Almacenamiento robusto y escalable

## Tecnologías

### Backend
- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos relacional
- **Alembic**: Migraciones de base de datos
- **JWT**: Autenticación con tokens
- **Pydantic**: Validación de datos

### Frontend
- **React**: Biblioteca de interfaz de usuario
- **React Router**: Navegación entre páginas
- **React Query**: Manejo de estado del servidor
- **Recharts**: Gráficos y visualizaciones
- **Lucide React**: Iconos modernos
- **Axios**: Cliente HTTP

## Instalación

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Backend

1. Navegar al directorio del backend:
```bash
cd backend
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Configurar base de datos:
```bash
# Crear base de datos en PostgreSQL
createdb task_tracker

# Ejecutar migraciones
alembic upgrade head
```

6. Ejecutar servidor:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Navegar al directorio del frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Ejecutar aplicación:
```bash
npm start
```

## Configuración

### Variables de Entorno (Backend)

Crear archivo `.env` en el directorio `backend/`:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/task_tracker
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Variables de Entorno (Frontend)

Crear archivo `.env` en el directorio `frontend/`:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Uso

### Acceso al Sistema

1. **Backend API**: http://localhost:8000
2. **Frontend**: http://localhost:3000
3. **Documentación API**: http://localhost:8000/docs

### Usuarios por Defecto

Para crear usuarios iniciales, ejecuta el script de inicialización:

```bash
python backend/scripts/init_data.py
```

Esto creará:
- Empresa de ejemplo (Colmena ARL, Positiva ARL)
- Usuario administrador (admin/admin123)
- Usuario regular (user/user123)

### Roles y Permisos

- **Admin**: Acceso completo a todas las funcionalidades
- **Manager**: Gestión de tareas y usuarios de su empresa
- **Usuario**: Gestión de sus propias tareas

## Estructura del Proyecto

```
Task Tracker/
├── backend/
│   ├── app/
│   │   ├── routers/          # Rutas de la API
│   │   ├── models.py         # Modelos de base de datos
│   │   ├── schemas.py        # Esquemas Pydantic
│   │   ├── auth.py           # Autenticación
│   │   ├── database.py       # Configuración de BD
│   │   └── main.py           # Aplicación principal
│   ├── alembic/              # Migraciones
│   ├── requirements.txt      # Dependencias Python
│   └── .env.example         # Variables de entorno
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── pages/           # Páginas de la aplicación
│   │   ├── contexts/        # Contextos React
│   │   ├── services/        # Servicios API
│   │   └── App.js           # Aplicación principal
│   ├── package.json         # Dependencias Node.js
│   └── public/              # Archivos públicos
└── README.md                # Este archivo
```

## API Endpoints

### Autenticación
- `POST /api/v1/token` - Obtener token de acceso
- `GET /api/v1/me` - Información del usuario actual

### Tareas
- `GET /api/v1/tasks` - Listar tareas
- `POST /api/v1/tasks` - Crear tarea
- `GET /api/v1/tasks/{id}` - Obtener tarea
- `PUT /api/v1/tasks/{id}` - Actualizar tarea
- `DELETE /api/v1/tasks/{id}` - Eliminar tarea

### Usuarios
- `GET /api/v1/users` - Listar usuarios
- `POST /api/v1/users` - Crear usuario
- `GET /api/v1/users/{id}` - Obtener usuario
- `PUT /api/v1/users/{id}` - Actualizar usuario
- `DELETE /api/v1/users/{id}` - Eliminar usuario

### Empresas
- `GET /api/v1/companies` - Listar empresas
- `POST /api/v1/companies` - Crear empresa
- `GET /api/v1/companies/{id}` - Obtener empresa
- `PUT /api/v1/companies/{id}` - Actualizar empresa
- `DELETE /api/v1/companies/{id}` - Eliminar empresa

### Dashboard
- `GET /api/v1/dashboard/stats` - Estadísticas generales
- `GET /api/v1/dashboard/company-stats` - Estadísticas por empresa
- `GET /api/v1/dashboard/user-tasks/{id}` - Estadísticas de usuario

## Desarrollo

### Ejecutar en Modo Desarrollo

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm start
```

### Migraciones de Base de Datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1
```

### Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Despliegue

### Docker (Recomendado)

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build
```

### Producción

1. Configurar variables de entorno de producción
2. Usar un servidor WSGI como Gunicorn
3. Configurar Nginx como proxy reverso
4. Usar una base de datos PostgreSQL en producción

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas, contacta al equipo de desarrollo o crea un issue en el repositorio.
