#!/bin/bash

echo "Iniciando la aplicación Flask..."

# Asegurarse de que el puerto esté configurado, si no, usar el puerto 8000 por defecto
PORT=${PORT:-8000}

# Instalar dependencias si es necesario
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

# Iniciar la aplicación con Waitress
waitress-serve --host=0.0.0.0 --port=$PORT --ident=PetPlatformBackend app:create_app
