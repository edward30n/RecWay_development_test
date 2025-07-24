# RecWay v1.0 - Sistema Completo de Análisis de Calidad de Carreteras

![CI/CD Status](https://github.com/edward30n/RecWay_development_test/workflows/RecWay%20CI/CD%20Pipeline/badge.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=flat&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Tabla de Contenido

1. [Introducción y Descripción General](#-introducción-y-descripción-general)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Estructura Detallada del Código](#-estructura-detallada-del-código)
4. [Base de Datos: Esquema y Diseño](#-base-de-datos-esquema-y-diseño)
5. [Arquitectura Docker Completa](#-arquitectura-docker-completa)
6. [Instalación y Configuración](#-instalación-y-configuración)
7. [Guía de Desarrollo Local](#-guía-de-desarrollo-local)
8. [Guía de Docker](#-guía-de-docker)
9. [API Endpoints y Documentación](#-api-endpoints-y-documentación)
10. [Testing y Validación](#-testing-y-validación)
11. [Despliegue y Producción](#-despliegue-y-producción)
12. [Contribución y Desarrollo](#-contribución-y-desarrollo)
13. [Troubleshooting](#-troubleshooting)
14. [Anexos y Referencias](#-anexos-y-referencias)

---

## 🎯 Introducción y Descripción General

### ¿Qué es RecWay?

RecWay es un sistema backend completo desarrollado en **FastAPI** para el análisis y monitoreo en tiempo real de la calidad de carreteras utilizando datos de sensores móviles. El sistema está diseñado para procesar información proveniente de dispositivos smartphones y sensores especializados que recolectan datos de acelerómetro, giroscopio y GPS mientras los vehículos transitan por diferentes segmentos de carretera.

### Características Principales

- **🔄 API REST Completa**: Endpoints para gestión de segmentos, muestras, sensores y análisis
- **📊 Procesamiento de Datos**: Cálculo automático de índices IRI (International Roughness Index)
- **🗄️ Base de Datos Robusta**: Esquema PostgreSQL optimizado con 9 tablas relacionales
- **🐳 Containerización**: Docker completo para desarrollo y producción
- **📱 Soporte Multi-dispositivo**: Compatible con datos de smartphones y sensores especializados
- **🔍 Análisis Geoespacial**: Gestión de coordenadas y geometrías de segmentos
- **⚡ Operaciones Asíncronas**: Alto rendimiento con async/await
- **📚 Documentación Automática**: Swagger UI y ReDoc integrados
- **🔐 Arquitectura Segura**: Validación automática con Pydantic

### Casos de Uso

1. **Monitoreo de Infraestructura**: Agencies gubernamentales pueden monitorear el estado de carreteras
2. **Investigación Académica**: Análisis de patrones de deterioro en pavimentos
3. **Aplicaciones Móviles**: Backend para apps de reporte ciudadano de calidad vial
4. **Mantenimiento Predictivo**: Identificación proactiva de segmentos que requieren intervención

---

## 🏗️ Arquitectura del Sistema

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA RECWAY v1.0                │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   FRONTEND       │    │    BACKEND       │    │    DATABASE     │
│  (Futuro)        │◄───┤   FastAPI        │◄───┤   PostgreSQL     │
│                  │    │   Puerto: 8000   │    │   Puerto: 5432   │
│  - Web App       │    │                  │    │                  │
│  - Mobile App    │    │  - API REST      │    │  - 9 Tablas      │
│  - Dashboard     │    │  - Validación    │    │  - Índices       │
└──────────────────┘    │  - Documentación │    │  - Relaciones    │
                        └──────────────────┘    └──────────────────┘
                                 │
                        ┌──────────────────┐
                        │    ADMINER       │
                        │   Puerto: 8080   │
                        │                  │
                        │  - Admin BD      │
                        │  - Query Tool    │
                        │  - Desarrollo    │
                        └──────────────────┘
```

### Stack Tecnológico

#### Backend (FastAPI)
- **Python 3.11+**: Lenguaje base con soporte completo para async/await
- **FastAPI**: Framework web moderno con generación automática de documentación
- **Pydantic**: Validación de datos y serialización automática
- **asyncpg**: Driver asíncrono para PostgreSQL de alto rendimiento
- **uvicorn**: Servidor ASGI para aplicaciones asíncronas

#### Base de Datos
- **PostgreSQL 15**: Base de datos relacional robusta
- **Esquema Optimizado**: 9 tablas con índices para consultas eficientes
- **Soporte GIS**: Preparado para extensiones geoespaciales futuras

#### Infraestructura
- **Docker**: Containerización completa del stack
- **Docker Compose**: Orquestación de servicios
- **GitHub Actions**: CI/CD automatizado
- **Adminer**: Interfaz web para administración de BD

---

## 📁 Estructura Detallada del Código

### Vista General del Proyecto

```
RecWay_development_test/
├── 📄 README.md                    # Documentación principal
├── 📄 .gitignore                   # Archivos excluidos de Git
├── 📄 docker-compose.yml           # Orquestación de servicios
├── 📄 setup-dev.bat               # Script de configuración Windows
├── 📄 setup-dev.sh                # Script de configuración Linux/Mac
├── 📁 .github/                    # GitHub Actions CI/CD
│   └── workflows/
│       └── ci-cd.yml              # Pipeline automatizado
└── 📁 backend/                    # Aplicación principal
    ├── 📄 Dockerfile              # Imagen Docker del backend
    ├── 📄 .dockerignore           # Archivos excluidos de Docker
    ├── 📄 requirements.txt        # Dependencias Python
    ├── 📄 .env.docker             # Variables de entorno Docker
    ├── 📄 .env.docker.example     # Plantilla de configuración
    └── 📁 app/                    # Código fuente principal
        ├── 📄 __init__.py
        ├── 📄 main.py             # Punto de entrada FastAPI
        ├── 📁 api/                # Definición de endpoints
        │   ├── 📄 __init__.py
        │   ├── 📄 api.py          # Router principal
        │   └── 📁 endpoints/      # Endpoints por dominio
        │       ├── 📄 __init__.py
        │       ├── 📄 segmentos.py    # CRUD segmentos
        │       ├── 📄 muestras.py     # CRUD muestras  
        │       └── 📄 sensores.py     # CRUD sensores
        ├── 📁 core/               # Configuración central
        │   ├── 📄 __init__.py
        │   └── 📄 config.py       # Settings y variables
        ├── 📁 db/                 # Base de datos
        │   ├── 📄 __init__.py
        │   ├── 📄 database.py     # Conexión y pool
        │   ├── 📄 init_complete.sql   # Schema completo
        │   └── 📄 sample_data.sql     # Datos de prueba
        ├── 📁 schemas/            # Modelos Pydantic
        │   ├── 📄 __init__.py
        │   ├── 📄 segmentos.py    # Schemas de segmentos
        │   ├── 📄 muestras.py     # Schemas de muestras
        │   ├── 📄 sensores.py     # Schemas de sensores
        │   └── 📄 responses.py    # Responses comunes
        └── 📁 services/           # Lógica de negocio
            ├── 📄 __init__.py
            ├── 📄 segmentos_service.py # Lógica segmentos
            ├── 📄 muestra_service.py   # Lógica muestras
            └── 📄 sensores_service.py  # Lógica sensores
```

### Análisis Detallado por Módulo

#### 🚀 app/main.py - Punto de Entrada

```python
# Responsabilidades principales:
# 1. Configuración de la aplicación FastAPI
# 2. Middleware CORS para frontend
# 3. Inclusión de routers
# 4. Gestión del ciclo de vida (startup/shutdown)
# 5. Endpoints de salud y documentación

# Características técnicas:
# - Lifespan manager para conexión/desconexión de BD
# - CORS configurado para desarrollo y producción
# - Documentación en /docs y /redoc
# - Health checks en /health
```

#### 🔧 app/core/config.py - Configuración Central

```python
# Gestión de configuración avanzada:
# 1. Variables de entorno con valores por defecto
# 2. Configuración específica para Docker
# 3. URLs de base de datos dinámicas
# 4. Settings para CORS y debugging
# 5. Compatibilidad con diferentes entornos

# Patrón implementado:
# - Singleton settings
# - Property-based URL construction
# - Environment-specific overrides
```

#### 🗄️ app/db/database.py - Gestión de Base de Datos

```python
# Pool de conexiones avanzado:
# 1. asyncpg.Pool para conexiones concurrentes
# 2. Gestión automática de conexiones
# 3. Patrón Connection Manager
# 4. Error handling y reconexión
# 5. Configuración optimizada para producción

# Características de rendimiento:
# - Min/Max pool size configurable
# - Connection recycling
# - Query timeout management
```
