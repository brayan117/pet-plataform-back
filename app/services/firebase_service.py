import firebase_admin
from firebase_admin import firestore, credentials
from flask import current_app
import json
import os
import logging

# Configurar logger
logger = logging.getLogger(__name__)

# Inicializar db como None
db = None

# Variable para rastrear si ya se intentó inicializar
_initialized = False

# Variable para almacenar las credenciales
_firebase_creds = None

def _get_credentials():
    """Obtiene las credenciales de Firebase desde las variables de entorno o archivo."""
    global _firebase_creds
    
    if _firebase_creds is not None:
        return _firebase_creds
    
    # Intentar obtener las credenciales de las variables de entorno
    firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
    
    if firebase_creds_json:
        try:
            # Intentar cargar como JSON
            cred_info = json.loads(firebase_creds_json)
            _firebase_creds = credentials.Certificate(cred_info)
            logger.info("Credenciales de Firebase cargadas desde variable de entorno")
            return _firebase_creds
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar FIREBASE_CREDENTIALS_JSON: {e}")
            # Continuar para intentar con el archivo
    
    # Si no hay variable de entorno o hay un error, intentar con el archivo
    cred_file = os.getenv('FIREBASE_CREDENTIALS', 'pet-plataform-back-firebase-adminsdk-fbsvc-bb8c26602e.json')
    cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), cred_file)
    
    if os.path.exists(cred_path):
        _firebase_creds = credentials.Certificate(cred_path)
        logger.info(f"Credenciales de Firebase cargadas desde archivo: {cred_file}")
        return _firebase_creds
    
    raise ValueError("No se encontraron credenciales de Firebase válidas en FIREBASE_CREDENTIALS_JSON ni en archivo")

def init_firebase():
    """
    Inicializa Firebase y configura la instancia de Firestore.
    
    Returns:
        firestore.Client: Instancia de Firestore
    """
    global db, _initialized
    
    # Si ya está inicializado, retornar la instancia existente
    if db is not None:
        return db
    
    try:
        # Obtener credenciales
        cred = _get_credentials()
        
        # Inicializar Firebase si no está inicializado
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            logger.info("Firebase inicializado correctamente")
        
        # Obtener la instancia de Firestore
        db = firestore.client()
        _initialized = True
        logger.info("Conexión con Firestore establecida correctamente")
        return db
        
    except Exception as e:
        error_msg = f"Error al inicializar Firestore: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

def get_db():
    """
    Obtiene la instancia de Firestore, inicializándola si es necesario.
    
    Returns:
        firestore.Client: Instancia de Firestore
    """
    global db
    
    if db is None and not _initialized:
        return init_firebase()
    return db

# Inicialización diferida - ya no se inicializa al importar
# La inicialización ahora ocurrirá con la primera llamada a get_db()