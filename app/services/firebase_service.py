import firebase_admin
from firebase_admin import firestore
from flask import current_app

# Inicializar db como None
db = None

def init_firebase():
    """
    Inicializa Firebase y configura la instancia de Firestore.
    
    Returns:
        firestore.Client: Instancia de Firestore
    """
    global db
    
    try:
        # Si ya está inicializado, retornar la instancia existente
        if db is not None:
            return db
            
        # Inicializar Firebase si no está inicializado
        if not firebase_admin._apps:
            from ..config.firebase_config import init_firebase as init_firebase_config
            init_firebase_config()
        
        # Obtener la instancia de Firestore
        db = firestore.client()
        return db
        
    except Exception as e:
        current_app.logger.error(f"Error al inicializar Firestore: {str(e)}")
        raise

# Inicializar Firestore al importar el módulo
try:
    db = init_firebase()
except Exception as e:
    print(f"Advertencia: No se pudo inicializar Firestore: {str(e)}")
    db = None