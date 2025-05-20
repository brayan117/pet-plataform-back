# 🐾 Pet Platform - Backend

Backend para la plataforma de gestión de mascotas, desarrollado con Python, Flask y Firebase.

## 🚀 Requisitos previos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)
- Cuenta de Firebase y archivo de credenciales de servicio
- Cuenta de Microsoft Azure para el despliegue

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


## 🔄 Despliegue en Azure Web App

### Requisitos previos

- [CLI de Azure](https://docs.microsoft.com/cli/azure/install-azure-cli) instalado
- Suscripción de Azure activa
- Aplicación web creada en Azure App Service

### Pasos para el despliegue

1. **Configurar las variables de entorno en Azure Portal**
   - Ve a tu App Service en Azure Portal
   - En el menú de configuración, selecciona "Configuración" > "Configuración de la aplicación"
   - Agrega las siguientes variables de configuración:
     - `FIREBASE_CREDENTIALS_JSON`: El contenido completo de tu archivo de credenciales de Firebase (todo en una línea)
     - `FLASK_ENV`: `production`
     - `PYTHON_VERSION`: `3.9`
     - `SCM_DO_BUILD_DURING_DEPLOYMENT`: `1`
     - `WEBSITE_RUN_FROM_PACKAGE`: `0`

2. **Configurar el runtime de Python**
   - Asegúrate de que el archivo `runtime.txt` esté presente en la raíz del proyecto con el contenido: `python-3.9.13`

3. **Desplegar usando Azure CLI**
   ```bash
   # Iniciar sesión en Azure
   az login
   
   # Configurar el contexto de la suscripción (si es necesario)
   az account set --subscription "NOMBRE_DE_TU_SUSCRIPCION"
   
   # Navegar al directorio del proyecto
   cd ruta/a/tu/proyecto
   
   # Desplegar el código
   az webapp up --sku F1 --name NOMBRE_DE_TU_APP --resource-group NOMBRE_DEL_GRUPO_DE_RECURSOS --runtime "PYTHON|3.9"
   ```

4. **Opcional: Configurar despliegue desde GitHub**
   - En Azure Portal, ve a tu App Service
   - Selecciona "Centro de implementación"
   - Sigue las instrucciones para conectar tu repositorio de GitHub
   - Configura la rama y la ruta si es necesario
   - Guarda la configuración para activar el despliegue automático

### Solución de problemas

- **Error de tiempo de espera durante el despliegue**: Asegúrate de que el archivo `startup.cmd` esté configurado correctamente.
- **Error de módulo no encontrado**: Verifica que todas las dependencias estén en `requirements.txt`.
- **Error de credenciales de Firebase**: Asegúrate de que el JSON de credenciales esté correctamente formateado en una sola línea.

### Monitoreo y registros

- **Registros de aplicación**: En Azure Portal, ve a tu App Service > Registros de aplicación
- **Streaming de registros**: Usa Azure CLI con `az webapp log tail --name NOMBRE_DE_TU_APP --resource-group NOMBRE_DEL_GRUPO_DE_RECURSOS`
- **Métricas**: Monitorea el rendimiento en "Supervisión" > "Métricas"

### Escalado

- **Escalado vertical**: Aumenta el plan de servicio para obtener más recursos
- **Escalado horizontal**: Configura el escalado automático en "Escalar horizontalmente"

### Copias de seguridad

Configura copias de seguridad automáticas en "Copias de seguridad" en el menú de configuración de tu App Service.

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
