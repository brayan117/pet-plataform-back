from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
import logging
from .config import config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    
    try:
        # Configuración de la aplicación
        if config_name is None:
            config_name = os.getenv('FLASK_ENV', 'development')
        
        # Cargar configuración desde objeto de configuración
        app.config.from_object(config[config_name])
        
        # Cargar configuración desde .env
        from dotenv import load_dotenv
        load_dotenv()
        
        # Configurar logging según el entorno
        if app.config.get('DEBUG'):
            logging.getLogger().setLevel(logging.DEBUG)
            logger.info("Modo DEBUG activado")
        
        # Cargar configuración de Firebase desde variables de entorno
        firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
        if firebase_creds_json:
            try:
                # Validar que el JSON es válido
                json.loads(firebase_creds_json)
                os.environ['FIREBASE_CREDENTIALS_JSON'] = firebase_creds_json
                logger.info("Configuración de Firebase cargada desde variable de entorno")
            except json.JSONDecodeError as e:
                logger.error(f"Error al decodificar FIREBASE_CREDENTIALS_JSON: {e}")
        
        # Cargar otras variables de entorno con prefijo FLASK_
        app.config.from_prefixed_env()
        
        # Habilitar CORS
        CORS(app)
        logger.info("CORS habilitado")
        
        # Ruta de verificación de estado
        @app.route('/health')
        def health_check():
            return jsonify({
                "status": "ok",
                "message": "Servicio en funcionamiento",
                "environment": config_name,
                "debug": app.debug
            })
        
        # Registrar rutas
        from .routes import register_routes
        register_routes(app)
        logger.info("Rutas registradas")
        
        logger.info(f"Aplicación configurada en modo {config_name}")
        
        return app
        
    except Exception as e:
        logger.error(f"Error al inicializar la aplicación: {e}", exc_info=True)
        raise
