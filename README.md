# 🐾 Pet Platform - Backend

Backend para la plataforma de gestión de mascotas, desarrollado con Python, FastAPI y Firebase.

## 🚀 Requisitos previos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)
- Cuenta de Firebase y archivo de credenciales de servicio
- API Key de The Dog API (https://thedogapi.com/)

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

4. **Configuración de variables de entorno**

   - Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
     ```
     # Configuración de la aplicación
     DEBUG=True
     SECRET_KEY=tu-clave-secreta-aqui
     
     # Configuración de Firebase
     FIREBASE_CREDENTIALS=pet-plataform-back-firebase-adminsdk-fbsvc-bb8c26602e.json
     
     # Configuración de The Dog API
     DOG_API_KEY=tu-api-key-aqui
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
   uvicorn main:app --reload
   ```

2. **Acceder a la API**
   - La API estará disponible en `http://localhost:8000`
   - Documentación Swagger UI: `http://localhost:8000/docs`
   - Documentación ReDoc: `http://localhost:8000/redoc`

## 📁 Estructura del proyecto

```
pet-plataform-back/
├── .env                    # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── requirements.txt        # Dependencias del proyecto
├── main.py                # Punto de entrada de la aplicación
├── app/
│   ├── __init__.py       # Inicialización de la aplicación
│   ├── config/           # Configuraciones
│   │   ├── __init__.py
│   │   └── firebase_config.py
│   └── models/           # Modelos de datos
│       └── dog.py
└── pet-plataform-back-firebase-adminsdk-fbsvc-bb8c26602e.json  # Credenciales de Firebase
```

## 🔒 Variables de entorno

| Variable             | Descripción                                  | Valor por defecto                |
|----------------------|----------------------------------------------|----------------------------------|
| DEBUG                | Modo depuración (True/False)                 | True                             |
| SECRET_KEY           | Clave secreta para la aplicación             |                                  |
| FIREBASE_CREDENTIALS | Ruta al archivo de credenciales de Firebase | pet-plataform-back-...json       |
| DOG_API_KEY          | API Key para The Dog API                     |                                  |





## 🐕 API de Perros

### Endpoints

#### 1. Listar todas las razas de perros
```http
GET /razas/perros
```

**Respuesta:**
```json
{
  "razas": [
    {
      "id": 1,
      "nombre": "Affenpinscher",
      "descripcion": "Small rodent hunting, lapdog",
      "temperamento": "Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
      "vida_promedio": "10 - 12 years",
      "origen": "Germany, France",
      "imagen": "https://cdn2.thedogapi.com/images/hd1iiHXjK.jpg"
    },
    // ... más razas
  ]
}
```

**Características:**
- Devuelve todas las razas de perros disponibles en The Dog API
- Incluye una imagen aleatoria para cada raza
- Proporciona información detallada como temperamento, esperanza de vida y origen
- No tiene límite en el número de razas devueltas

## 🔄 Despliegue

Para entornos de producción, se recomienda:

1. Configurar `DEBUG=False`
2. Configurar un servidor WSGI como Gunicorn o uWSGI
3. Usar un servidor web como Nginx como proxy inverso

## 🤝 Contribución

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

Desarrollado con ❤️ por [Yeimer campo]
