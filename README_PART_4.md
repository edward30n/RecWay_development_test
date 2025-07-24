# README PARTE 4: Uso, Testing y Despliegue en Producción

---

## 🧪 Testing y Validación

### Estrategia de Testing Implementada

```
┌─────────────────────────────────────────────────────────────┐
│                     TESTING PYRAMID                        │
└─────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │   E2E Tests     │  ← Pocos, críticos
                    │   (Selenium)    │
                    └─────────────────┘
                  ┌─────────────────────┐
                  │  Integration Tests  │  ← Moderados
                  │   (FastAPI Client)  │
                  └─────────────────────┘
              ┌─────────────────────────────┐
              │      Unit Tests             │  ← Muchos, rápidos
              │   (pytest + coverage)      │
              └─────────────────────────────┘
```

### Test Suite Completo

#### test_segmentos.py - Testing de Endpoints
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.db.database import get_database
from app.core.config import settings

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE TESTING
# ═══════════════════════════════════════════════════════════════

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override de la conexión a BD para testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Aplicar override
app.dependency_overrides[get_database] = override_get_db

# Cliente de testing
client = TestClient(app)

# ═══════════════════════════════════════════════════════════════
# FIXTURES Y HELPERS
# ═══════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def test_db():
    """Crear base de datos de testing"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_segmento():
    """Segmento de prueba"""
    return {
        "nombre": "Segmento Test",
        "descripcion": "Segmento para testing",
        "longitud": -74.123456,
        "latitud": 4.654321,
        "ubicacion": "Bogotá Test"
    }

@pytest.fixture
def auth_headers():
    """Headers de autenticación para tests"""
    return {"Authorization": "Bearer test-token"}

# ═══════════════════════════════════════════════════════════════
# TESTS DE HEALTH CHECK
# ═══════════════════════════════════════════════════════════════

def test_health_check():
    """Test básico de conectividad"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "uptime" in data

def test_health_check_database():
    """Test de conectividad a base de datos"""
    response = client.get("/health/database")
    assert response.status_code == 200
    data = response.json()
    assert data["database"]["status"] == "connected"

# ═══════════════════════════════════════════════════════════════
# TESTS CRUD DE SEGMENTOS
# ═══════════════════════════════════════════════════════════════

class TestSegmentosCRUD:
    
    def test_create_segmento_success(self, sample_segmento):
        """Test de creación exitosa"""
        response = client.post("/api/v1/segmentos/", json=sample_segmento)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == sample_segmento["nombre"]
        assert "id_segmento" in data
        assert "created_at" in data
    
    def test_create_segmento_validation_error(self):
        """Test de validación de datos"""
        invalid_data = {
            "nombre": "",  # Nombre vacío
            "longitud": 200,  # Longitud inválida
            "latitud": 100   # Latitud inválida
        }
        response = client.post("/api/v1/segmentos/", json=invalid_data)
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("nombre" in str(error) for error in errors)
        assert any("longitud" in str(error) for error in errors)
    
    def test_get_segmento_success(self, sample_segmento):
        """Test de obtención por ID"""
        # Crear segmento primero
        create_response = client.post("/api/v1/segmentos/", json=sample_segmento)
        segmento_id = create_response.json()["id_segmento"]
        
        # Obtener segmento
        response = client.get(f"/api/v1/segmentos/{segmento_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_segmento"] == segmento_id
        assert data["nombre"] == sample_segmento["nombre"]
    
    def test_get_segmento_not_found(self):
        """Test de segmento no encontrado"""
        response = client.get("/api/v1/segmentos/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_list_segmentos_pagination(self):
        """Test de paginación"""
        # Crear múltiples segmentos
        for i in range(5):
            segmento = {
                "nombre": f"Segmento {i}",
                "longitud": -74.0 + i,
                "latitud": 4.0 + i
            }
            client.post("/api/v1/segmentos/", json=segmento)
        
        # Test paginación
        response = client.get("/api/v1/segmentos/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_update_segmento_success(self, sample_segmento):
        """Test de actualización"""
        # Crear segmento
        create_response = client.post("/api/v1/segmentos/", json=sample_segmento)
        segmento_id = create_response.json()["id_segmento"]
        
        # Actualizar
        update_data = {"nombre": "Segmento Actualizado"}
        response = client.put(f"/api/v1/segmentos/{segmento_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Segmento Actualizado"
    
    def test_delete_segmento_success(self, sample_segmento):
        """Test de eliminación"""
        # Crear segmento
        create_response = client.post("/api/v1/segmentos/", json=sample_segmento)
        segmento_id = create_response.json()["id_segmento"]
        
        # Eliminar
        response = client.delete(f"/api/v1/segmentos/{segmento_id}")
        assert response.status_code == 204
        
        # Verificar eliminación
        get_response = client.get(f"/api/v1/segmentos/{segmento_id}")
        assert get_response.status_code == 404

# ═══════════════════════════════════════════════════════════════
# TESTS DE PERFORMANCE
# ═══════════════════════════════════════════════════════════════

import time

class TestPerformance:
    
    def test_response_time_health(self):
        """Test de tiempo de respuesta del health check"""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Menos de 1 segundo
    
    def test_concurrent_requests(self):
        """Test de manejo de requests concurrentes"""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/health")
        
        # Simular 10 requests concurrentes
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [f.result() for f in futures]
        
        # Todas deben ser exitosas
        assert all(r.status_code == 200 for r in responses)
    
    def test_large_dataset_handling(self):
        """Test de manejo de datasets grandes"""
        # Crear muchos segmentos
        segmentos = []
        for i in range(100):
            segmento = {
                "nombre": f"Segmento Masivo {i}",
                "longitud": -74.0 + (i * 0.001),
                "latitud": 4.0 + (i * 0.001)
            }
            response = client.post("/api/v1/segmentos/", json=segmento)
            assert response.status_code == 201
        
        # Verificar que se pueden listar todos
        start_time = time.time()
        response = client.get("/api/v1/segmentos/?limit=100")
        end_time = time.time()
        
        assert response.status_code == 200
        assert len(response.json()) == 100
        assert (end_time - start_time) < 5.0  # Menos de 5 segundos

# ═══════════════════════════════════════════════════════════════
# TESTS DE INTEGRACIÓN
# ═══════════════════════════════════════════════════════════════

class TestIntegration:
    
    def test_complete_workflow(self):
        """Test de workflow completo: crear → listar → modificar → eliminar"""
        # 1. Crear segmento
        segmento_data = {
            "nombre": "Workflow Test",
            "longitud": -74.123,
            "latitud": 4.456
        }
        create_response = client.post("/api/v1/segmentos/", json=segmento_data)
        assert create_response.status_code == 201
        segmento_id = create_response.json()["id_segmento"]
        
        # 2. Verificar en listado
        list_response = client.get("/api/v1/segmentos/")
        assert any(s["id_segmento"] == segmento_id for s in list_response.json())
        
        # 3. Modificar
        update_response = client.put(
            f"/api/v1/segmentos/{segmento_id}",
            json={"nombre": "Workflow Test Updated"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["nombre"] == "Workflow Test Updated"
        
        # 4. Eliminar
        delete_response = client.delete(f"/api/v1/segmentos/{segmento_id}")
        assert delete_response.status_code == 204
        
        # 5. Verificar eliminación
        get_response = client.get(f"/api/v1/segmentos/{segmento_id}")
        assert get_response.status_code == 404
```

### Configuración de Testing Automático

#### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --strict-markers
    --strict-config
    --cov=app
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    performance: marks tests as performance tests
```

#### Scripts de Testing

**test.ps1 (PowerShell)**
```powershell
#!/usr/bin/env powershell
<#
.SYNOPSIS
    Script completo de testing para RecWay
#>

param(
    [string]$TestType = "all",     # all, unit, integration, performance
    [switch]$Coverage,             # Generar reporte de cobertura
    [switch]$Verbose,              # Salida detallada
    [switch]$FailFast             # Parar en el primer error
)

function Run-Tests {
    param([string]$Pattern, [string]$Description)
    
    Write-Host "`n🧪 Ejecutando $Description..." -ForegroundColor Yellow
    
    $args = @("pytest")
    if ($Pattern) { $args += "-m", $Pattern }
    if ($Coverage) { $args += "--cov=app", "--cov-report=html" }
    if ($Verbose) { $args += "-v" }
    if ($FailFast) { $args += "-x" }
    
    & docker-compose exec backend $args
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Tests fallaron" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ Tests exitosos" -ForegroundColor Green
    }
}

# Verificar que los servicios estén corriendo
Write-Host "🔍 Verificando servicios..." -ForegroundColor Cyan
$services = docker-compose ps --services --filter "status=running"
if (-not $services -or $services -notcontains "backend") {
    Write-Host "❌ Los servicios no están corriendo. Ejecute setup-dev.ps1 primero." -ForegroundColor Red
    exit 1
}

# Ejecutar tests según el tipo
switch ($TestType.ToLower()) {
    "unit" {
        Run-Tests "unit" "tests unitarios"
    }
    "integration" {
        Run-Tests "integration" "tests de integración"
    }
    "performance" {
        Run-Tests "performance" "tests de performance"
    }
    "all" {
        Run-Tests "" "todos los tests"
    }
    default {
        Write-Host "❌ Tipo de test inválido: $TestType" -ForegroundColor Red
        Write-Host "Tipos válidos: all, unit, integration, performance" -ForegroundColor Gray
        exit 1
    }
}

if ($Coverage) {
    Write-Host "`n📊 Reporte de cobertura generado en htmlcov/index.html" -ForegroundColor Green
    Start-Process "htmlcov/index.html"
}
```

---

## 🔧 Troubleshooting Común

### Problemas Frecuentes y Soluciones

#### 1. Docker Desktop no Inicia
**Síntomas:**
- Error: "Docker Desktop failed to start"
- Error: "Hardware assisted virtualization and data execution protection must be enabled"

**Soluciones:**
```powershell
# Verificar Hyper-V
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V

# Habilitar Hyper-V si está deshabilitado
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# Verificar virtualización en BIOS
# Reiniciar y entrar a BIOS → Enable Intel VT-x o AMD-V

# Resetear Docker Desktop
# Settings → Reset → Reset to factory defaults
```

#### 2. Puerto Ya en Uso
**Síntomas:**
- Error: "Port 8000 is already in use"
- Error: "bind: address already in use"

**Diagnóstico y Solución:**
```powershell
# Encontrar proceso usando el puerto
netstat -ano | findstr :8000
Get-Process -Id [PID_ENCONTRADO]

# Terminar proceso específico
Stop-Process -Id [PID] -Force

# O cambiar puerto en docker-compose.yml
# ports:
#   - "8001:8000"  # Usar puerto 8001 en host
```

#### 3. Base de Datos no Se Conecta
**Síntomas:**
- Error: "could not connect to server"
- Error: "FATAL: database 'recway_db' does not exist"

**Diagnóstico:**
```powershell
# Verificar estado del contenedor
docker-compose ps

# Ver logs de PostgreSQL
docker-compose logs recway_db

# Conectar manualmente a la BD
docker-compose exec recway_db psql -U postgres -d recway_db
```

**Soluciones:**
```powershell
# Recrear volumen de BD
docker-compose down -v
docker volume rm recway_postgres_data
docker-compose up -d

# Verificar variables de entorno
docker-compose exec backend env | grep DATABASE

# Probar conexión desde el backend
docker-compose exec backend python -c "
import asyncpg
import asyncio
async def test():
    conn = await asyncpg.connect('postgresql://postgres:postgres123@recway_db:5432/recway_db')
    print('Connection successful')
    await conn.close()
asyncio.run(test())
"
```

#### 4. Aplicación Backend No Responde
**Síntomas:**
- Error 502 Bad Gateway
- Timeout en requests HTTP

**Diagnóstico:**
```powershell
# Ver logs del backend
docker-compose logs -f backend

# Verificar estado del contenedor
docker-compose exec backend ps aux

# Probar conexión directa
docker-compose exec backend curl http://localhost:8000/health
```

**Soluciones:**
```powershell
# Reiniciar solo el backend
docker-compose restart backend

# Reconstruir imagen del backend
docker-compose build --no-cache backend
docker-compose up -d backend

# Verificar dependencias Python
docker-compose exec backend pip list
```

#### 5. Problemas de Permisos en Windows
**Síntomas:**
- Error: "Permission denied"
- Archivos no se pueden crear en volúmenes

**Soluciones:**
```powershell
# Verificar permisos del directorio
icacls .\docker_data

# Otorgar permisos completos
icacls .\docker_data /grant Users:F /T

# Ejecutar Docker Desktop como administrador
# Clic derecho → "Run as administrator"

# Configurar compartir unidades en Docker Desktop
# Settings → Resources → File Sharing → Add current drive
```

### Comandos de Debugging Útiles

#### Inspección de Contenedores
```powershell
# Estado detallado de servicios
docker-compose ps --all

# Logs con timestamps
docker-compose logs --timestamps backend

# Seguir logs en tiempo real
docker-compose logs -f --tail=100 backend

# Información del sistema Docker
docker system info

# Uso de recursos
docker stats
```

#### Debugging de Red
```powershell
# Inspeccionar red de Docker
docker network ls
docker network inspect recway_recway_network

# Probar conectividad entre contenedores
docker-compose exec backend ping recway_db
docker-compose exec backend nslookup recway_db

# Verificar puertos expuestos
docker-compose port backend 8000
```

#### Debugging de Base de Datos
```sql
-- Conectar a PostgreSQL
docker-compose exec recway_db psql -U postgres -d recway_db

-- Verificar tablas
\dt

-- Verificar conexiones activas
SELECT * FROM pg_stat_activity WHERE datname = 'recway_db';

-- Verificar tamaño de BD
SELECT pg_size_pretty(pg_database_size('recway_db'));

-- Ver consultas lentas
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC LIMIT 10;
```

---

## 🚀 Despliegue en Producción

### Preparación para Producción

#### 1. Variables de Entorno de Producción
```bash
# .env.production
DATABASE_URL=postgresql://recway_user:STRONG_PASSWORD@db.recway.com:5432/recway_prod
POSTGRES_DB=recway_prod
POSTGRES_USER=recway_user
POSTGRES_PASSWORD=GENERATED_STRONG_PASSWORD

# Seguridad
DEBUG=false
SECRET_KEY=GENERATED_CRYPTOGRAPHICALLY_SECURE_KEY
ALLOWED_HOSTS=api.recway.com,www.recway.com

# SSL y CORS
CORS_ORIGINS=https://app.recway.com,https://admin.recway.com
USE_SSL=true
SSL_REDIRECT=true

# Logging
LOG_LEVEL=warning
LOG_FORMAT=json
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project

# Performance
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
REDIS_URL=redis://redis.recway.com:6379/0

# Monitoring
PROMETHEUS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
```

#### 2. Dockerfile de Producción
```dockerfile
# Dockerfile.prod - Optimizado para producción
FROM python:3.11-slim as base

# Labels para metadata
LABEL org.opencontainers.image.title="RecWay API"
LABEL org.opencontainers.image.description="Road Quality Analysis API"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="RecWay Team"

# Variables de build
ARG BUILD_DATE
ARG VCS_REF
LABEL org.opencontainers.image.created=$BUILD_DATE
LABEL org.opencontainers.image.revision=$VCS_REF

# Variables de entorno optimizadas para producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONPATH=/app

# Instalar dependencias del sistema solo las necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove

# Crear usuario no-root
RUN groupadd -r recway && useradd -r -g recway -d /app -s /sbin/nologin recway

# Configurar directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copiar aplicación
COPY --chown=recway:recway . .

# Configurar permisos
RUN chmod +x /app/entrypoint.prod.sh

# Cambiar a usuario no-root
USER recway

# Health check optimizado
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Exponer puerto
EXPOSE 8000

# Script de entrada
ENTRYPOINT ["/app/entrypoint.prod.sh"]
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
```

#### 3. Configuración de Gunicorn
```python
# gunicorn.conf.py - Configuración de producción
import multiprocessing
import os

# Configuración del servidor
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 120
keepalive = 5

# Logging
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
preload_app = True
worker_tmp_dir = "/dev/shm"

# Graceful shutdown
graceful_timeout = 30

def worker_int(worker):
    """Handle worker interruption gracefully"""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def when_ready(server):
    """Called when the server is ready"""
    server.log.info("Server is ready. Spawning workers")

def worker_exit(server, worker):
    """Called when a worker exits"""
    server.log.info("Worker %s exited", worker.pid)
```

#### 4. Docker Compose para Producción
```yaml
# docker-compose.prod.yml
version: '3.8'

x-common-variables: &common-variables
  environment: &common-environment
    - TZ=America/Bogota
    - LANG=es_ES.UTF-8

services:
  # ═══════════════════════════════════════════════════════════════
  # REVERSE PROXY (NGINX)
  # ═══════════════════════════════════════════════════════════════
  nginx:
    image: nginx:1.25-alpine
    container_name: recway_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
    networks:
      - recway_prod_network
    <<: *common-variables

  # ═══════════════════════════════════════════════════════════════
  # BACKEND API
  # ═══════════════════════════════════════════════════════════════
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
      args:
        BUILD_DATE: ${BUILD_DATE}
        VCS_REF: ${VCS_REF}
    container_name: recway_backend_prod
    restart: unless-stopped
    env_file:
      - .env.production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - backend_logs:/app/logs
      - backend_uploads:/app/uploads
    networks:
      - recway_prod_network
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    <<: *common-variables

  # ═══════════════════════════════════════════════════════════════
  # BASE DE DATOS POSTGRESQL
  # ═══════════════════════════════════════════════════════════════
  db:
    image: postgres:15-alpine
    container_name: recway_db_prod
    restart: unless-stopped
    env_file:
      - .env.production
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d:ro
      - postgres_backups:/backups
    networks:
      - recway_prod_network
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER -d $POSTGRES_DB"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    <<: *common-variables

  # ═══════════════════════════════════════════════════════════════
  # REDIS CACHE
  # ═══════════════════════════════════════════════════════════════
  redis:
    image: redis:7.2-alpine
    container_name: recway_redis_prod
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - recway_prod_network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    <<: *common-variables

  # ═══════════════════════════════════════════════════════════════
  # MONITORING
  # ═══════════════════════════════════════════════════════════════
  prometheus:
    image: prom/prometheus:latest
    container_name: recway_prometheus
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - recway_prod_network
    deploy:
      resources:
        limits:
          memory: 512M

  grafana:
    image: grafana/grafana:latest
    container_name: recway_grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    networks:
      - recway_prod_network
    depends_on:
      - prometheus

# ═══════════════════════════════════════════════════════════════
# VOLÚMENES DE PRODUCCIÓN
# ═══════════════════════════════════════════════════════════════
volumes:
  postgres_data_prod:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/recway/data/postgres

  redis_data:
    driver: local

  backend_logs:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/recway/logs

  nginx_logs:
    driver: local

  prometheus_data:
    driver: local

  grafana_data:
    driver: local

  postgres_backups:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/recway/backups

  backend_uploads:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/recway/uploads

# ═══════════════════════════════════════════════════════════════
# RED DE PRODUCCIÓN
# ═══════════════════════════════════════════════════════════════
networks:
  recway_prod_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.25.0.0/16
```

### Scripts de Despliegue

#### deploy.sh - Script de Despliegue Automático
```bash
#!/bin/bash
# Script de despliegue automático para RecWay
# Uso: ./deploy.sh [staging|production]

set -e

# Configuración
ENVIRONMENT=${1:-staging}
PROJECT_NAME="recway"
BACKUP_RETENTION_DAYS=7
DEPLOY_USER="deploy"
DOCKER_REGISTRY="registry.recway.com"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Verificar requisitos previos
check_prerequisites() {
    log "Verificando requisitos previos..."
    
    command -v docker >/dev/null 2>&1 || error "Docker no está instalado"
    command -v docker-compose >/dev/null 2>&1 || error "Docker Compose no está instalado"
    
    # Verificar conexión a registro
    docker login $DOCKER_REGISTRY || error "No se puede conectar al registro Docker"
    
    log "Requisitos verificados ✓"
}

# Crear backup de la base de datos
backup_database() {
    log "Creando backup de la base de datos..."
    
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    BACKUP_PATH="/opt/recway/backups/$BACKUP_FILE"
    
    docker-compose exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > $BACKUP_PATH
    gzip $BACKUP_PATH
    
    log "Backup creado: ${BACKUP_PATH}.gz"
    
    # Limpiar backups antiguos
    find /opt/recway/backups -name "backup_*.sql.gz" -mtime +$BACKUP_RETENTION_DAYS -delete
}

# Construir y subir imágenes
build_and_push() {
    log "Construyendo imágenes Docker..."
    
    # Construir imagen del backend
    BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    VCS_REF=$(git rev-parse --short HEAD)
    
    docker build \
        --build-arg BUILD_DATE=$BUILD_DATE \
        --build-arg VCS_REF=$VCS_REF \
        -t $DOCKER_REGISTRY/$PROJECT_NAME/backend:$VCS_REF \
        -t $DOCKER_REGISTRY/$PROJECT_NAME/backend:latest \
        -f backend/Dockerfile.prod \
        backend/
    
    # Subir al registro
    docker push $DOCKER_REGISTRY/$PROJECT_NAME/backend:$VCS_REF
    docker push $DOCKER_REGISTRY/$PROJECT_NAME/backend:latest
    
    log "Imágenes construidas y subidas ✓"
}

# Desplegar servicios
deploy_services() {
    log "Desplegando servicios..."
    
    # Exportar variables para docker-compose
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD)
    export COMPOSE_PROJECT_NAME=$PROJECT_NAME
    
    # Usar archivo de compose específico del entorno
    COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"
    
    if [ ! -f $COMPOSE_FILE ]; then
        error "Archivo de compose no encontrado: $COMPOSE_FILE"
    fi
    
    # Realizar despliegue rolling
    docker-compose -f $COMPOSE_FILE pull
    docker-compose -f $COMPOSE_FILE up -d --remove-orphans
    
    log "Servicios desplegados ✓"
}

# Verificar salud de los servicios
health_check() {
    log "Verificando salud de los servicios..."
    
    # Esperar a que los servicios estén listos
    sleep 30
    
    # Verificar API
    for i in {1..10}; do
        if curl -s -f http://localhost:8000/health >/dev/null; then
            log "API está funcionando ✓"
            break
        fi
        
        if [ $i -eq 10 ]; then
            error "API no responde después de 10 intentos"
        fi
        
        warn "Intento $i/10: API no responde, reintentando en 10s..."
        sleep 10
    done
    
    # Verificar base de datos
    docker-compose exec -T db pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || error "Base de datos no está lista"
    
    log "Verificación de salud completada ✓"
}

# Limpieza post-despliegue
cleanup() {
    log "Realizando limpieza..."
    
    # Limpiar imágenes antiguas
    docker image prune -a -f --filter "until=24h"
    
    # Limpiar volúmenes no utilizados
    docker volume prune -f
    
    log "Limpieza completada ✓"
}

# Notificación de despliegue
notify_deployment() {
    log "Enviando notificación de despliegue..."
    
    WEBHOOK_URL="${SLACK_WEBHOOK_URL}"
    if [ -n "$WEBHOOK_URL" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚀 Despliegue de RecWay completado en $ENVIRONMENT\nCommit: $(git rev-parse --short HEAD)\nFecha: $(date)\"}" \
            $WEBHOOK_URL
    fi
}

# Función principal
main() {
    log "Iniciando despliegue en $ENVIRONMENT"
    
    check_prerequisites
    
    if [ "$ENVIRONMENT" = "production" ]; then
        backup_database
    fi
    
    build_and_push
    deploy_services
    health_check
    cleanup
    notify_deployment
    
    log "🎉 Despliegue completado exitosamente en $ENVIRONMENT"
    log "🌐 API disponible en: http://localhost:8000"
    log "📊 Documentación: http://localhost:8000/docs"
}

# Manejo de señales para limpieza
trap 'error "Despliegue interrumpido"' INT TERM

# Ejecutar función principal
main
```

### Configuración de CI/CD con GitHub Actions

#### .github/workflows/deploy.yml
```yaml
name: Deploy RecWay

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: recway/backend

jobs:
  # ═══════════════════════════════════════════════════════════════
  # TESTING
  # ═══════════════════════════════════════════════════════════════
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov pytest-asyncio
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml

  # ═══════════════════════════════════════════════════════════════
  # BUILD AND PUSH
  # ═══════════════════════════════════════════════════════════════
  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: ./backend
        file: ./backend/Dockerfile.prod
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        build-args: |
          BUILD_DATE=${{ fromJSON(steps.meta.outputs.json).labels['org.opencontainers.image.created'] }}
          VCS_REF=${{ fromJSON(steps.meta.outputs.json).labels['org.opencontainers.image.revision'] }}

  # ═══════════════════════════════════════════════════════════════
  # DEPLOY TO STAGING
  # ═══════════════════════════════════════════════════════════════
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
    - name: Deploy to staging
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.STAGING_HOST }}
        username: ${{ secrets.STAGING_USER }}
        key: ${{ secrets.STAGING_SSH_KEY }}
        script: |
          cd /opt/recway
          git pull origin develop
          ./deploy.sh staging

  # ═══════════════════════════════════════════════════════════════
  # DEPLOY TO PRODUCTION
  # ═══════════════════════════════════════════════════════════════
  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.PRODUCTION_HOST }}
        username: ${{ secrets.PRODUCTION_USER }}
        key: ${{ secrets.PRODUCTION_SSH_KEY }}
        script: |
          cd /opt/recway
          git pull origin main
          ./deploy.sh production

    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      if: always()
```

---

## 📚 Recursos Adicionales y Documentación

### Enlaces de Referencia
- **FastAPI**: https://fastapi.tiangolo.com/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Docker**: https://docs.docker.com/
- **Pydantic**: https://docs.pydantic.dev/
- **Asyncpg**: https://magicstack.github.io/asyncpg/

### Comunidad y Soporte
- **GitHub Issues**: Para reportar bugs y solicitar features
- **Documentation**: Wiki del proyecto con ejemplos detallados
- **API Reference**: Documentación auto-generada en `/docs`

---

**¡Felicidades! Has completado la configuración de RecWay v1.0** 🎉

Este README completo te proporciona toda la información necesaria para:
- ✅ Entender la arquitectura del proyecto
- ✅ Configurar el entorno de desarrollo
- ✅ Ejecutar y testing la aplicación
- ✅ Solucionar problemas comunes
- ✅ Desplegar en producción

Para cualquier pregunta adicional, consulta la documentación técnica en `/docs` o abre un issue en GitHub.
