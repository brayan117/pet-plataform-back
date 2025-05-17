from flask import Flask
from flask_cors import CORS
import os
from .config import config

def create_app(config_name=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    
    # Configuración de la aplicación
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    app.config.from_prefixed_env()  # Carga variables con prefijo FLASK_
    
    # Habilitar CORS
    CORS(app)
    
    try:
        # Registrar rutas
        from .routes import register_routes
        register_routes(app)
        
        return app
        
    except Exception as e:
        print(f"Error al inicializar la aplicación: {e}")
        raise
