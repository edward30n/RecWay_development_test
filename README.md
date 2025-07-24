# RecWay - Sistema de Análisis de Calidad de Carreteras

![CI/CD Status](https://github.com/edward30n/RecWay_development_test/workflows/RecWay%20CI/CD%20Pipeline/badge.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=flat&logo=postgresql&logoColor=white)

RecWay es una API backend desarrollada con FastAPI para el análisis y monitoreo de la calidad de carreteras utilizando datos de sensores móviles.

## 🚀 Inicio Rápido con Docker

### Una línea de comando:
```bash
git clone https://github.com/edward30n/RecWay_development_test.git && cd RecWay_development_test && ./setup-dev.sh
```

### Paso a paso:
```bash
# 1. Clonar el repositorio
git clone https://github.com/edward30n/RecWay_development_test.git
cd RecWay_development_test

# 2. Ejecutar configuración automática
./setup-dev.sh        # Linux/Mac
# o
setup-dev.bat          # Windows

# El script automáticamente:
# - Verifica que Docker esté corriendo
# - Crea archivo .env.docker si no existe
# - Construye e inicia todos los servicios
# - Muestra URLs y comandos útiles
```

### URLs disponibles:
- **🔗 API Backend:** http://localhost:8000
- **📚 Documentación:** http://localhost:8000/docs
- **🔄 ReDoc:** http://localhost:8000/redoc
- **🗄️ Adminer (BD):** http://localhost:8080

## 📦 Usando la imagen de GitHub Container Registry

```bash
# Usar la última versión
docker pull ghcr.io/edward30n/recway_development_test:latest

# Usar una versión específica
docker pull ghcr.io/edward30n/recway_development_test:v1.0.0
```

## 📊 Estructura del Proyecto

```
cloud_app_v1/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints organizados por dominio
│   │   ├── core/             # Configuración central
│   │   ├── db/               # Conexión a BD y scripts SQL
│   │   ├── schemas/          # Modelos Pydantic
│   │   ├── services/         # Lógica de negocio
│   │   └── main.py           # Aplicación principal
│   ├── requirements.txt      # Dependencias Python
│   ├── Dockerfile           # Imagen Docker
│   └── .env                 # Variables de entorno
├── docker-compose.yml       # Orquestación de servicios
└── README.md               # Documentación
```

## 🐳 Instalación con Docker (Recomendado)

### Prerrequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Git

### Instalación automática

**Windows:**
```bash
git clone https://github.com/edward30n/RecWay_development_test.git
cd RecWay_development_test
setup-dev.bat
```

**Linux/Mac:**
```bash
git clone https://github.com/edward30n/RecWay_development_test.git
cd RecWay_development_test
chmod +x setup-dev.sh
./setup-dev.sh
```

**Manual:**
```bash
git clone https://github.com/edward30n/RecWay_development_test.git
cd RecWay_development_test
cp backend/.env.docker.example backend/.env.docker
# Editar backend/.env.docker si es necesario
docker-compose up --build -d
```

### URLs disponibles:
- **🔗 API Backend:** http://localhost:8000
- **📚 Documentación:** http://localhost:8000/docs
- **🔄 ReDoc:** http://localhost:8000/redoc
- **🗄️ Adminer (BD):** http://localhost:8080

## 💻 Instalación Local (Desarrollo)

### Prerrequisitos
- Python 3.11+
- PostgreSQL 15+

### Pasos

1. **Crear entorno virtual:**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activar entorno virtual:**
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales de BD
   ```

5. **Ejecutar la aplicación:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🗄️ Base de Datos

### Esquema Principal
- **segmento**: Segmentos de carretera con información geográfica
- **muestra**: Muestras de datos recolectadas por dispositivos
- **geometria**: Puntos que definen la geometría de segmentos
- **registro_sensores**: Datos detallados de sensores
- **fuente_datos_dispositivo**: Metainformación de dispositivos

### Inicialización
El script `init_recway_v2.sql` se ejecuta automáticamente con Docker.

## 📡 API Endpoints

### Segmentos
- `GET /api/v1/segmentos/` - Listar segmentos
- `POST /api/v1/segmentos/` - Crear segmento
- `GET /api/v1/segmentos/{id}` - Obtener segmento
- `PUT /api/v1/segmentos/{id}` - Actualizar segmento
- `DELETE /api/v1/segmentos/{id}` - Eliminar segmento

### Muestras
- `GET /api/v1/muestras/` - Listar muestras
- `POST /api/v1/muestras/` - Crear muestra
- `GET /api/v1/muestras/{id}` - Obtener muestra

### Sensores
- `GET /api/v1/sensores/` - Listar sensores
- `POST /api/v1/sensores/` - Crear sensor

## 🧪 Pruebas

### Con Postman
1. Importar la colección desde `/docs`
2. Configurar el entorno base: `http://localhost:8000`

### Ejemplo de Petición
```bash
curl -X POST "http://localhost:8000/api/v1/segmentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carretera Central Km 50",
    "descripcion": "Segmento de prueba",
    "longitud": -76.935242,
    "latitud": -12.046374,
    "ubicacion": "Lima, Perú"
  }'
```

## 🛠️ Comandos Docker Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f backend
docker-compose logs -f recway_db

# Reiniciar servicios
docker-compose restart backend
docker-compose restart recway_db

# Detener todo
docker-compose down

# Detener y eliminar volúmenes (⚠️ Elimina datos de BD)
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache

# Ver estado de contenedores
docker-compose ps

# Ejecutar comandos dentro de contenedores
docker-compose exec backend bash
docker-compose exec recway_db psql -U postgres -d recWay_db

# Limpiar todo Docker (⚠️ Elimina TODO)
docker system prune -a
```

## 🔧 Configuración

### Variables de Entorno (.env)
```env
PROJECT_NAME=RecWay API
DEBUG=true
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=recWay_db
POSTGRES_PORT=5432
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 👥 Equipo

- **Edward30n** - Desarrollo inicial

## 📞 Soporte

Para soporte o preguntas, crear un issue en el repositorio.
