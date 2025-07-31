@echo off
echo Configurando el entorno de pruebas para la autenticación...
echo.

REM Establecer variables de entorno
set PROJECT_NAME="RecWay API Test"
set DEBUG=True
set HOST=localhost
set PORT=8000

REM Copiar el archivo .env.test como .env
copy /Y .env.test .env

echo Ejecutando el servidor de pruebas...
echo Presiona Ctrl+C para detener el servidor

REM Ejecutar el servidor
python test_auth.py

echo Servidor detenido.
