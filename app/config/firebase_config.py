import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import current_app

def init_firebase():
    """
    Inicializa la aplicación de Firebase con las credenciales.
    
    Esta función es mantenida por compatibilidad, pero se recomienda usar firebase_service.get_db()
    """
    from . import firebase_service
    return firebase_service.get_db() is not None

# Esta función se mantiene por compatibilidad, pero el nuevo código debería usar firebase_service.get_db()
# directamente en lugar de esta función
