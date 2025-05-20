#!/bin/bash

echo "Iniciando la aplicación Flask..."

# Asegurarse de que el puerto esté configurado, si no, usar el puerto 8000 por defecto
PORT=${PORT:-8000}

# Instalar dependencias
echo "Instalando dependencias..."
pip install --no-cache-dir -r requirements.txt

# Iniciar la aplicación con Waitress
echo "Iniciando la aplicación en el puerto $PORT..."
waitress-serve --host=0.0.0.0 --port=$PORT --ident=PetPlatformBackend app:create_app
