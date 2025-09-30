# 🚀 Despliegue en Railway - Task Tracker Ko-Actuar

## 📋 Requisitos Previos

1. **Cuenta en Railway**: Crear cuenta en [railway.app](https://railway.app)
2. **Railway CLI**: Instalar CLI de Railway
3. **Git**: Para subir el código

## 🛠️ Instalación de Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# O usando curl
curl -fsSL https://railway.app/install.sh | sh
```

## 🚀 Pasos para Desplegar

### 1. Preparar el Proyecto

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd task-tracker

# Hacer el script ejecutable
chmod +x deploy-railway.sh
```

### 2. Configurar Railway

```bash
# Login a Railway
railway login

# Crear nuevo proyecto
railway project new

# Conectar con GitHub (opcional)
railway connect
```

### 3. Configurar Variables de Entorno

```bash
# Configurar variables de entorno
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set DATABASE_URL="postgresql://postgres:password@localhost:5432/tasktracker_db"
railway variables set POSTGRES_DB="tasktracker_db"
railway variables set POSTGRES_USER="postgres"
railway variables set POSTGRES_PASSWORD="password"
railway variables set POSTGRES_HOST="localhost"
railway variables set POSTGRES_PORT="5432"
railway variables set BACKEND_PORT="8000"
railway variables set BACKEND_HOST="0.0.0.0"
railway variables set NODE_ENV="production"
railway variables set ADMIN_USERNAME="admin"
railway variables set ADMIN_EMAIL="admin@ko-actuar.com"
railway variables set ADMIN_PASSWORD="admin123"
railway variables set ADMIN_FULL_NAME="Administrador"
```

### 4. Desplegar

```bash
# Opción 1: Usar el script automatizado
./deploy-railway.sh

# Opción 2: Desplegar manualmente
railway up
```

## 🗄️ Configuración de Base de Datos

Railway automáticamente creará una base de datos PostgreSQL. Las variables de entorno se configurarán automáticamente.

## 🌐 Acceso a la Aplicación

Una vez desplegado, Railway te proporcionará una URL como:
- `https://your-project-name.railway.app`

## 👤 Credenciales por Defecto

- **Usuario**: `admin`
- **Contraseña**: `admin123`

## 🔧 Configuración Adicional

### Variables de Entorno Importantes

```bash
# Base de datos (configurado automáticamente por Railway)
DATABASE_URL=postgresql://...

# Seguridad
SECRET_KEY=tu-clave-secreta-muy-segura

# CORS (ajustar según tu dominio)
CORS_ORIGINS=https://tu-dominio.railway.app

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### Dominio Personalizado

1. En Railway Dashboard, ve a tu proyecto
2. Selecciona "Settings" > "Domains"
3. Agrega tu dominio personalizado
4. Configura los registros DNS según las instrucciones

## 📊 Monitoreo

Railway proporciona:
- **Logs en tiempo real**
- **Métricas de rendimiento**
- **Alertas automáticas**
- **Backups de base de datos**

## 🔄 Actualizaciones

Para actualizar la aplicación:

```bash
# Hacer cambios en el código
git add .
git commit -m "Actualización"
git push

# Railway detectará automáticamente los cambios y redesplegará
```

## 🆘 Solución de Problemas

### Error de Conexión a Base de Datos
```bash
# Verificar variables de entorno
railway variables

# Ver logs
railway logs
```

### Error de Build
```bash
# Ver logs de build
railway logs --build
```

### Problemas de CORS
```bash
# Actualizar CORS_ORIGINS
railway variables set CORS_ORIGINS="https://tu-dominio.railway.app"
```

## 💰 Costos

Railway ofrece:
- **Plan gratuito**: $5 de crédito mensual
- **Plan Pro**: $20/mes
- **Pago por uso**: Solo pagas lo que usas

## 📞 Soporte

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Discord**: [Railway Discord](https://discord.gg/railway)
- **GitHub Issues**: Para problemas específicos del proyecto

## ✅ Checklist de Despliegue

- [ ] Cuenta de Railway creada
- [ ] Railway CLI instalado
- [ ] Proyecto clonado
- [ ] Variables de entorno configuradas
- [ ] Aplicación desplegada
- [ ] Base de datos funcionando
- [ ] Login de admin funcionando
- [ ] Dominio personalizado configurado (opcional)
- [ ] Monitoreo configurado

---

**¡Tu aplicación Task Tracker Ko-Actuar estará lista para usar en Railway!** 🎉

