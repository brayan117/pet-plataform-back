from flask import Flask
from flask_cors import CORS
import os
import logging
from .config import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    
    # Configuración de la aplicación
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    app.config.from_prefixed_env()  # Carga variables con prefijo FLASK_
    
    # Configurar logging
    if app.config.get('LOG_LEVEL') == 'DEBUG':
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Habilitar CORS
    CORS(app)
    
    try:
        # Inicializar Firebase (a través del servicio)
        from .services.firebase_service import init_firebase
        firebase_app = init_firebase()
        if firebase_app:
            logger.info("Firebase inicializado correctamente")
        else:
            logger.warning("Firebase no pudo ser inicializado correctamente")
        
        # Registrar rutas
        from .routes import register_routes
        register_routes(app)
        
        return app
        
    except Exception as e:
        logger.error(f"Error al inicializar la aplicación: {e}", exc_info=True)
        raise
