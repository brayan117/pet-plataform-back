# 🐾 Pet Platform - Backend

Backend para la plataforma de gestión de mascotas, desarrollado con Python, Flask y Firebase.

## 🚀 Requisitos previos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)
- Cuenta de Firebase y archivo de credenciales de servicio

## 🛠️ Configuración del entorno

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/pet-plataform-back.git
   cd pet-plataform-back
   ```

2. **Crear y activar un entorno virtual (recomendado)**
   ```bash
   # En Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # En macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
   
   Si el archivo requirements.txt no existe, instala las dependencias manualmente:
   ```bash
   pip install flask flask-cors python-dotenv firebase-admin
   ```

4. **Configuración de variables de entorno**

   - Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
     ```
     # Configuración de la aplicación
     FLASK_ENV=development
     FLASK_DEBUG=1
     SECRET_KEY=tu-clave-secreta-aqui
     
     # Configuración de Firebase
     FIREBASE_CREDENTIALS=tu-archivo-credenciales.json
     ```

5. **Configuración de Firebase**
   - Ve a la [consola de Firebase](https://console.firebase.google.com/)
   - Selecciona tu proyecto o crea uno nuevo
   - Ve a Configuración del proyecto > Cuentas de servicio
   - Genera una nueva clave privada y descarga el archivo JSON
   - Coloca el archivo JSON en la raíz del proyecto
   - Asegúrate de que el nombre del archivo coincida con el valor de `FIREBASE_CREDENTIALS` en tu archivo `.env`

## 🚦 Ejecución del proyecto

1. **Iniciar el servidor de desarrollo**
   ```bash
   python run.py
   ```

2. **Acceder a la API**
   - La API estará disponible en `http://localhost:5000`
   - Ruta de verificación de estado: `GET /health`
   - Ruta principal: `GET /`

## 📁 Estructura del proyecto

```
pet-plataform-back/
├── .env                    # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── requirements.txt        # Dependencias del proyecto
├── run.py                 # Punto de entrada de la aplicación
├── app/
│   ├── __init__.py       # Inicialización de la aplicación
│   ├── config/           # Configuraciones
│   │   ├── __init__.py
│   │   └── firebase_config.py
│   ├── routes.py         # Definición de rutas de la API
│   └── services/         # Lógica de negocio
│       └── firebase_service.py
└── tu-archivo-credenciales.json  # Credenciales de Firebase
```

## 🔒 Variables de entorno

| Variable             | Descripción                                  | Valor por defecto                |
|----------------------|----------------------------------------------|----------------------------------|
| FLASK_ENV            | Entorno de ejecución (development/production) | development                      |
| FLASK_DEBUG          | Modo depuración (1/0)                       | 1                                |
| SECRET_KEY           | Clave secreta para la aplicación             |                                  |
| FIREBASE_CREDENTIALS | Ruta al archivo de credenciales de Firebase | pet-plataform-back-...json       |


## 🔄 Despliegue

Para entornos de producción, se recomienda:

1. Configurar `FLASK_ENV=production`
2. Establecer `FLASK_DEBUG=0`
3. Configurar un servidor WSGI como Gunicorn o uWSGI
4. Usar un servidor web como Nginx como proxy inverso

## 🤝 Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

Desarrollado con ❤️ por [Tu Nombre]
