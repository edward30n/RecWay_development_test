@echo off
REM Script para desarrolladores que clonan el repo por primera vez

echo 🚀 Configurando RecWay para desarrollo...

REM Verificar que Docker esté corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker no está ejecutándose
    echo Por favor inicia Docker Desktop e intenta de nuevo
    pause
    exit /b 1
)

REM Crear archivo de variables de entorno si no existe
if not exist "backend\.env.docker" (
    echo 📝 Creando archivo de configuración...
    copy "backend\.env.docker.example" "backend\.env.docker" >nul
    echo ✅ Archivo backend\.env.docker creado
    echo ⚠️  IMPORTANTE: Edita backend\.env.docker con tus credenciales
)

REM Construir e iniciar servicios
echo 📦 Construyendo e iniciando servicios...
docker-compose up --build -d

REM Esperar a que los servicios estén listos
echo ⏳ Esperando a que los servicios estén listos...
timeout /t 15 /nobreak >nul

REM Verificar estado
echo 🔍 Verificando estado de los servicios...
docker-compose ps

echo.
echo ✅ RecWay está ejecutándose!
echo.
echo 📊 URLs disponibles:
echo 🔗 Backend API: http://localhost:8000
echo 📚 Documentación: http://localhost:8000/docs
echo 🗄️  Adminer ^(BD^): http://localhost:8080
echo.
echo 🔧 Comandos útiles:
echo   Ver logs del backend: docker-compose logs -f backend
echo   Ver logs de la BD: docker-compose logs -f recway_db
echo   Detener todo: docker-compose down
echo   Reiniciar backend: docker-compose restart backend
echo   Estado de servicios: docker-compose ps
echo.
echo 📝 Para desarrollo:
echo   Los cambios en el código se reflejan automáticamente
echo   Edita backend/.env.docker para cambiar configuración
echo.
pause
