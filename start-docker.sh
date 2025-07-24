#!/bin/bash
# Script de inicio para Docker

echo "🚀 Iniciando RecWay con Docker..."

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose"
    echo "Por favor inicia Docker Desktop e intenta de nuevo"
    exit 1
fi

# Construir e iniciar los servicios
echo "📦 Construyendo e iniciando servicios..."
docker-compose up --build -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los servicios
echo "🔍 Verificando estado de los servicios..."
docker-compose ps

echo ""
echo "✅ RecWay está ejecutándose!"
echo ""
echo "📊 URLs disponibles:"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/docs"
echo "🔄 ReDoc: http://localhost:8000/redoc"
echo "🗄️  Adminer (BD): http://localhost:8080"
echo ""
echo "📋 Para ver logs:"
echo "   docker-compose logs -f backend"
echo ""
echo "🛑 Para detener:"
echo "   docker-compose down"
