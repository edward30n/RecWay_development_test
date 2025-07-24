# README PARTE 3: Docker, Instalación y Despliegue

---

## 🐳 Arquitectura Docker Completa

### Diseño de Contenedores

```yaml
# Arquitectura multi-container:
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER ARCHITECTURE                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Backend API   │    │   PostgreSQL    │    │     Adminer     │
│   (FastAPI)     │◄──►│   Database      │    │   (DB Admin)    │
│   Port: 8000    │    │   Port: 5432    │    │   Port: 8080    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                               │
                    ┌─────────────────┐
                    │  Docker Network │
                    │   'recway_net'  │
                    └─────────────────┘
```

### docker-compose.yml - Análisis Línea por Línea

```yaml
version: '3.8'

# Definición de servicios
services:
  # ═══════════════════════════════════════════════════════════════
  # SERVICIO: Base de Datos PostgreSQL
  # ═══════════════════════════════════════════════════════════════
  recway_db:
    image: postgres:15-alpine           # Imagen optimizada y ligera
    container_name: recway_postgres     # Nombre fijo para referencias
    restart: unless-stopped             # Política de reinicio automático
    
    # Variables de entorno para configuración inicial
    environment:
      POSTGRES_DB: recway_db           # Nombre de la base de datos
      POSTGRES_USER: postgres          # Usuario administrador
      POSTGRES_PASSWORD: postgres123   # Contraseña (cambiar en producción)
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --lc-collate=es_ES.UTF-8"
    
    # Mapeo de puertos: host:container
    ports:
      - "5432:5432"                    # PostgreSQL estándar
    
    # Volúmenes para persistencia de datos
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Datos persistentes
      - ./init_complete.sql:/docker-entrypoint-initdb.d/init.sql:ro  # Schema inicial
    
    # Configuración de red
    networks:
      - recway_network
    
    # Health check para verificar disponibilidad
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d recway_db"]
      interval: 30s                    # Verificar cada 30 segundos
      timeout: 10s                     # Timeout de 10 segundos
      retries: 3                       # 3 intentos antes de marcar como unhealthy
      start_period: 60s                # Esperar 60s antes del primer check

  # ═══════════════════════════════════════════════════════════════
  # SERVICIO: Backend FastAPI
  # ═══════════════════════════════════════════════════════════════
  backend:
    build:
      context: ./backend               # Directorio con Dockerfile
      dockerfile: Dockerfile           # Archivo de construcción
    container_name: recway_backend     # Nombre del contenedor
    restart: unless-stopped            # Reinicio automático
    
    # Variables de entorno específicas del backend
    environment:
      # Configuración de base de datos
      DATABASE_URL: postgresql://postgres:postgres123@recway_db:5432/recway_db
      
      # Configuración de FastAPI
      DEBUG: "true"                    # Modo desarrollo
      SECRET_KEY: "your-secret-key-here-change-in-production"
      CORS_ORIGINS: "http://localhost:3000,http://localhost:8080"
      
      # Configuración de logging
      LOG_LEVEL: "info"
      LOG_FORMAT: "json"
    
    # Mapeo de puertos
    ports:
      - "8000:8000"                    # API accesible en puerto 8000
    
    # Dependencias de servicios
    depends_on:
      recway_db:
        condition: service_healthy     # Esperar a que DB esté saludable
    
    # Volúmenes para desarrollo
    volumes:
      - ./backend:/app                 # Hot reload en desarrollo
      - backend_logs:/app/logs         # Persistencia de logs
    
    # Configuración de red
    networks:
      - recway_network
    
    # Health check del backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # ═══════════════════════════════════════════════════════════════
  # SERVICIO: Adminer (Administrador de BD)
  # ═══════════════════════════════════════════════════════════════
  adminer:
    image: adminer:4.8.1               # Versión específica para estabilidad
    container_name: recway_adminer     # Nombre del contenedor
    restart: unless-stopped            # Reinicio automático
    
    # Variables de entorno
    environment:
      ADMINER_DEFAULT_SERVER: recway_db  # Servidor por defecto
      ADMINER_DESIGN: pepa-linha        # Tema visual
    
    # Mapeo de puertos
    ports:
      - "8080:8080"                    # Interfaz web en puerto 8080
    
    # Dependencias
    depends_on:
      - recway_db                      # Requiere la base de datos
    
    # Red
    networks:
      - recway_network

# ═══════════════════════════════════════════════════════════════
# DEFINICIÓN DE VOLÚMENES PERSISTENTES
# ═══════════════════════════════════════════════════════════════
volumes:
  postgres_data:                      # Datos de PostgreSQL
    driver: local                     # Almacenamiento local
    driver_opts:
      type: none
      o: bind
      device: ./docker_data/postgres  # Carpeta local para backup fácil
  
  backend_logs:                       # Logs del backend
    driver: local
    driver_opts:
      type: none  
      o: bind
      device: ./docker_data/logs

# ═══════════════════════════════════════════════════════════════
# DEFINICIÓN DE REDES
# ═══════════════════════════════════════════════════════════════
networks:
  recway_network:                     # Red interna para comunicación
    driver: bridge                    # Driver de red bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16       # Subred específica para evitar conflictos
```

### Dockerfile Backend - Optimizado para Producción

```dockerfile
# ═══════════════════════════════════════════════════════════════
# STAGE 1: Base Image con dependencias del sistema
# ═══════════════════════════════════════════════════════════════
FROM python:3.11-slim as base

# Metadatos del contenedor
LABEL maintainer="RecWay Team"
LABEL version="1.0"
LABEL description="FastAPI Backend for RecWay Road Quality Analysis"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1              # Salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1       # No crear archivos .pyc
ENV PIP_NO_CACHE_DIR=1              # No cachear paquetes pip
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 # No verificar versión pip

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \                          # Para health checks
    gcc \                          # Para compilar extensiones
    g++ \                          # Para compilar extensiones C++
    libpq-dev \                    # PostgreSQL development headers
    && rm -rf /var/lib/apt/lists/* # Limpiar cache

# ═══════════════════════════════════════════════════════════════
# STAGE 2: Instalación de dependencias Python
# ═══════════════════════════════════════════════════════════════
FROM base as dependencies

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ═══════════════════════════════════════════════════════════════
# STAGE 3: Imagen final optimizada
# ═══════════════════════════════════════════════════════════════
FROM dependencies as final

# Crear usuario no-root para seguridad
RUN groupadd -r recway && useradd -r -g recway recway

# Crear directorios necesarios
RUN mkdir -p /app/logs && \
    chown -R recway:recway /app

# Copiar código de la aplicación
COPY --chown=recway:recway . .

# Cambiar al usuario no-root
USER recway

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 🚀 Guía de Instalación Completa

### Prerequisitos del Sistema

#### Windows (Recomendado: Windows 10/11 Pro)
```powershell
# Verificar versión de Windows
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion

# Habilitar Hyper-V (requerido para Docker Desktop)
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# Habilitar WSL2 (recomendado)
wsl --install
```

#### Instalación de Docker Desktop
1. **Descargar**: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
2. **Instalar** con configuraciones recomendadas:
   - ✅ Use WSL 2 instead of Hyper-V
   - ✅ Add shortcut to desktop
3. **Verificar instalación**:
```powershell
docker --version
docker-compose --version
```

#### Instalación de Git
```powershell
# Descargar desde: https://git-scm.com/download/win
# O usar winget:
winget install Git.Git

# Verificar
git --version
```

#### Editor de Código (Opcional pero recomendado)
```powershell
# Visual Studio Code
winget install Microsoft.VisualStudioCode

# Extensiones recomendadas:
# - Python
# - Docker
# - GitLens
# - REST Client
```

### Instalación del Proyecto

#### Paso 1: Clonar el Repositorio
```powershell
# Navegar al directorio deseado
cd C:\Users\$env:USERNAME\Desktop

# Clonar el proyecto
git clone https://github.com/tu-usuario/recway-cloud-app.git
cd recway-cloud-app

# Verificar estructura
tree /F
```

#### Paso 2: Configuración de Variables de Entorno
```powershell
# Crear archivo .env en el directorio raíz
@"
# Base de Datos
DATABASE_URL=postgresql://postgres:postgres123@recway_db:5432/recway_db
POSTGRES_DB=recway_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123

# FastAPI
DEBUG=true
SECRET_KEY=your-super-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
"@ | Out-File -FilePath .env -Encoding UTF8
```

#### Paso 3: Preparar Estructura de Directorios
```powershell
# Crear directorios para volúmenes persistentes
New-Item -ItemType Directory -Force -Path ".\docker_data\postgres"
New-Item -ItemType Directory -Force -Path ".\docker_data\logs"

# Verificar permisos
icacls .\docker_data /grant Users:F /T
```

#### Paso 4: Construir y Ejecutar los Servicios
```powershell
# Construir imágenes (primera vez)
docker-compose build --no-cache

# Iniciar todos los servicios
docker-compose up -d

# Verificar estado de los servicios
docker-compose ps
```

**Salida esperada:**
```
Name                Command                  State                    Ports
--------------------------------------------------------------------------------
recway_adminer    entrypoint.sh php -S ...   Up      0.0.0.0:8080->8080/tcp
recway_backend    uvicorn app.main:app ...   Up      0.0.0.0:8000->8000/tcp
recway_postgres   docker-entrypoint.s ...    Up      0.0.0.0:5432->5432/tcp
```

#### Paso 5: Verificación de la Instalación

**1. Verificar API Backend:**
```powershell
# Test básico de conectividad
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET

# Test de documentación
Start-Process "http://localhost:8000/docs"
```

**2. Verificar Base de Datos:**
```powershell
# Abrir Adminer en navegador
Start-Process "http://localhost:8080"

# Credenciales:
# Sistema: PostgreSQL
# Servidor: recway_db
# Usuario: postgres
# Contraseña: postgres123
# Base de datos: recway_db
```

**3. Verificar Logs:**
```powershell
# Ver logs de todos los servicios
docker-compose logs

# Ver logs específicos del backend
docker-compose logs backend

# Seguir logs en tiempo real
docker-compose logs -f backend
```

### Scripts de Desarrollo Automatizados

#### setup-dev.ps1 (PowerShell)
```powershell
#!/usr/bin/env powershell
<#
.SYNOPSIS
    Script de configuración automática para desarrollo de RecWay
.DESCRIPTION
    Configura el entorno completo de desarrollo, verifica dependencias
    y ejecuta todos los servicios necesarios.
#>

param(
    [switch]$CleanStart,    # Limpiar datos existentes
    [switch]$SkipBuild,     # Omitir reconstrucción de imágenes
    [switch]$Verbose        # Salida detallada
)

# Configuración
$ErrorActionPreference = "Stop"
$ProjectName = "RecWay Cloud App"
$RequiredPorts = @(5432, 8000, 8080)

function Write-Status {
    param([string]$Message, [string]$Color = "Green")
    Write-Host "✓ $Message" -ForegroundColor $Color
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient("localhost", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

function Test-Prerequisites {
    Write-Host "`n🔍 Verificando prerequisitos..." -ForegroundColor Yellow
    
    # Verificar Docker
    try {
        $dockerVersion = docker --version
        Write-Status "Docker encontrado: $dockerVersion"
    } catch {
        Write-Error "Docker no está instalado o no está en PATH"
        exit 1
    }
    
    # Verificar Docker Compose
    try {
        $composeVersion = docker-compose --version
        Write-Status "Docker Compose encontrado: $composeVersion"
    } catch {
        Write-Error "Docker Compose no está disponible"
        exit 1
    }
    
    # Verificar puertos
    Write-Host "`n🔍 Verificando puertos disponibles..." -ForegroundColor Yellow
    foreach ($port in $RequiredPorts) {
        if (Test-Port $port) {
            Write-Error "Puerto $port está en uso"
            $processes = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
            if ($processes) {
                Write-Host "   Procesos usando el puerto:" -ForegroundColor Gray
                $processes | ForEach-Object { 
                    $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
                    if ($proc) {
                        Write-Host "   - $($proc.ProcessName) (PID: $($proc.Id))" -ForegroundColor Gray
                    }
                }
            }
            exit 1
        } else {
            Write-Status "Puerto $port disponible"
        }
    }
}

function Initialize-Environment {
    Write-Host "`n🔧 Configurando entorno..." -ForegroundColor Yellow
    
    # Crear directorios necesarios
    $directories = @("docker_data\postgres", "docker_data\logs")
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Force -Path $dir | Out-Null
            Write-Status "Directorio creado: $dir"
        }
    }
    
    # Verificar archivo .env
    if (!(Test-Path ".env")) {
        Write-Host "⚠️  Archivo .env no encontrado. Creando con valores por defecto..." -ForegroundColor Yellow
        $envContent = @"
DATABASE_URL=postgresql://postgres:postgres123@recway_db:5432/recway_db
POSTGRES_DB=recway_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=info
LOG_FORMAT=json
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Status "Archivo .env creado"
    }
}

function Start-Services {
    Write-Host "`n🚀 Iniciando servicios..." -ForegroundColor Yellow
    
    if ($CleanStart) {
        Write-Host "🧹 Limpiando datos existentes..." -ForegroundColor Yellow
        docker-compose down -v
        Remove-Item -Recurse -Force "docker_data\*" -ErrorAction SilentlyContinue
        Initialize-Environment
    }
    
    if (!$SkipBuild) {
        Write-Host "🔨 Construyendo imágenes..." -ForegroundColor Yellow
        docker-compose build
    }
    
    Write-Host "▶️  Iniciando contenedores..." -ForegroundColor Yellow
    docker-compose up -d
    
    # Esperar a que los servicios estén listos
    Write-Host "⏳ Esperando a que los servicios estén listos..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Verificar health checks
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        try {
            $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
            Write-Status "Backend API está funcionando"
            break
        } catch {
            $attempt++
            if ($attempt -eq $maxAttempts) {
                Write-Error "Backend API no responde después de $maxAttempts intentos"
                docker-compose logs backend
                exit 1
            }
            Start-Sleep -Seconds 2
        }
    }
}

function Show-Summary {
    Write-Host "`n🎉 ¡$ProjectName configurado exitosamente!" -ForegroundColor Green
    Write-Host "`n📋 Servicios disponibles:" -ForegroundColor Cyan
    Write-Host "   • API Backend:     http://localhost:8000" -ForegroundColor White
    Write-Host "   • Documentación:   http://localhost:8000/docs" -ForegroundColor White
    Write-Host "   • Admin DB:        http://localhost:8080" -ForegroundColor White
    Write-Host "   • PostgreSQL:      localhost:5432" -ForegroundColor White
    
    Write-Host "`n🔧 Comandos útiles:" -ForegroundColor Cyan
    Write-Host "   • Ver logs:        docker-compose logs -f" -ForegroundColor Gray
    Write-Host "   • Detener:         docker-compose down" -ForegroundColor Gray
    Write-Host "   • Reiniciar:       docker-compose restart" -ForegroundColor Gray
    Write-Host "   • Estado:          docker-compose ps" -ForegroundColor Gray
    
    # Abrir navegador automáticamente
    Start-Process "http://localhost:8000/docs"
}

# Ejecución principal
try {
    Write-Host "🚀 Iniciando configuración de $ProjectName" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    
    Test-Prerequisites
    Initialize-Environment
    Start-Services
    Show-Summary
    
} catch {
    Write-Error "Error durante la configuración: $($_.Exception.Message)"
    Write-Host "`n📋 Para debugging, ejecute:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs" -ForegroundColor Gray
    exit 1
}
```

#### setup-dev.sh (Bash para Git Bash/WSL)
```bash
#!/bin/bash
# Script de configuración para desarrollo RecWay
# Compatible con Git Bash y WSL en Windows

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
PROJECT_NAME="RecWay Cloud App"
REQUIRED_PORTS=(5432 8000 8080)

# Funciones auxiliares
log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

check_port() {
    local port=$1
    if command -v netstat >/dev/null 2>&1; then
        netstat -an | grep ":$port " >/dev/null 2>&1
    elif command -v ss >/dev/null 2>&1; then
        ss -an | grep ":$port " >/dev/null 2>&1
    else
        # Fallback usando telnet
        timeout 1 bash -c "echo >/dev/tcp/localhost/$port" >/dev/null 2>&1
    fi
}

verify_prerequisites() {
    echo -e "\n${YELLOW}🔍 Verificando prerequisitos...${NC}"
    
    # Verificar Docker
    if ! command -v docker >/dev/null 2>&1; then
        log_error "Docker no está instalado"
        exit 1
    fi
    log_success "Docker encontrado: $(docker --version)"
    
    # Verificar Docker Compose
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker Compose no está instalado"
        exit 1
    fi
    log_success "Docker Compose encontrado: $(docker-compose --version)"
    
    # Verificar puertos
    echo -e "\n${YELLOW}🔍 Verificando puertos disponibles...${NC}"
    for port in "${REQUIRED_PORTS[@]}"; do
        if check_port $port; then
            log_error "Puerto $port está en uso"
            exit 1
        else
            log_success "Puerto $port disponible"
        fi
    done
}

setup_environment() {
    echo -e "\n${YELLOW}🔧 Configurando entorno...${NC}"
    
    # Crear directorios
    mkdir -p docker_data/{postgres,logs}
    log_success "Directorios de datos creados"
    
    # Verificar .env
    if [ ! -f ".env" ]; then
        log_warning "Archivo .env no encontrado. Creando con valores por defecto..."
        cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres123@recway_db:5432/recway_db
POSTGRES_DB=recway_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=info
LOG_FORMAT=json
EOF
        log_success "Archivo .env creado"
    fi
}

start_services() {
    echo -e "\n${YELLOW}🚀 Iniciando servicios...${NC}"
    
    # Limpiar si se solicita
    if [ "$1" = "--clean" ]; then
        log_info "Limpiando datos existentes..."
        docker-compose down -v 2>/dev/null || true
        rm -rf docker_data/* 2>/dev/null || true
        setup_environment
    fi
    
    # Construir imágenes
    if [ "$1" != "--skip-build" ]; then
        log_info "Construyendo imágenes..."
        docker-compose build
    fi
    
    # Iniciar servicios
    log_info "Iniciando contenedores..."
    docker-compose up -d
    
    # Esperar a que estén listos
    echo -e "\n${YELLOW}⏳ Esperando a que los servicios estén listos...${NC}"
    sleep 10
    
    # Verificar API
    local attempts=0
    local max_attempts=30
    
    while [ $attempts -lt $max_attempts ]; do
        if curl -s http://localhost:8000/health >/dev/null 2>&1; then
            log_success "Backend API está funcionando"
            break
        fi
        
        attempts=$((attempts + 1))
        if [ $attempts -eq $max_attempts ]; then
            log_error "Backend API no responde después de $max_attempts intentos"
            docker-compose logs backend
            exit 1
        fi
        sleep 2
    done
}

show_summary() {
    echo -e "\n${GREEN}🎉 ¡$PROJECT_NAME configurado exitosamente!${NC}"
    echo -e "\n${BLUE}📋 Servicios disponibles:${NC}"
    echo "   • API Backend:     http://localhost:8000"
    echo "   • Documentación:   http://localhost:8000/docs"
    echo "   • Admin DB:        http://localhost:8080"
    echo "   • PostgreSQL:      localhost:5432"
    
    echo -e "\n${BLUE}🔧 Comandos útiles:${NC}"
    echo "   • Ver logs:        docker-compose logs -f"
    echo "   • Detener:         docker-compose down"
    echo "   • Reiniciar:       docker-compose restart"
    echo "   • Estado:          docker-compose ps"
    
    # Abrir navegador si está disponible
    if command -v start >/dev/null 2>&1; then
        start "http://localhost:8000/docs"
    elif command -v open >/dev/null 2>&1; then
        open "http://localhost:8000/docs"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://localhost:8000/docs"
    fi
}

# Ejecución principal
main() {
    echo -e "${BLUE}🚀 Iniciando configuración de $PROJECT_NAME${NC}"
    echo "================================================"
    
    verify_prerequisites
    setup_environment
    start_services "$@"
    show_summary
}

# Manejo de argumentos
case "${1:-}" in
    --help|-h)
        echo "Uso: $0 [opciones]"
        echo "Opciones:"
        echo "  --clean       Limpiar datos existentes antes de iniciar"
        echo "  --skip-build  Omitir la reconstrucción de imágenes"
        echo "  --help        Mostrar esta ayuda"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
```
