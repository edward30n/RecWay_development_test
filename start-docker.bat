@echo off
REM Script de inicio para Docker en Windows

echo 🚀 Iniciando RecWay con Docker...

REM Verificar que Docker esté corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker no está ejecutándose
    echo Por favor inicia Docker Desktop e intenta de nuevo
    pause
    exit /b 1
)

REM Construir e iniciar los servicios
echo 📦 Construyendo e iniciando servicios...
docker-compose up --build -d

REM Esperar a que los servicios estén listos
echo ⏳ Esperando a que los servicios estén listos...
timeout /t 10 /nobreak >nul

REM Verificar estado de los servicios
echo 🔍 Verificando estado de los servicios...
docker-compose ps

echo.
echo ✅ RecWay está ejecutándose!
echo.
echo 📊 URLs disponibles:
echo 🔗 Backend API: http://localhost:8000
echo 📚 Documentación: http://localhost:8000/docs
echo 🔄 ReDoc: http://localhost:8000/redoc
echo 🗄️  Adminer ^(BD^): http://localhost:8080
echo.
echo 📋 Para ver logs:
echo    docker-compose logs -f backend
echo.
echo 🛑 Para detener:
echo    docker-compose down
echo.
pause
