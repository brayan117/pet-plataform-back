import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import current_app

def init_firebase():
    """Inicializa la aplicación de Firebase con las credenciales."""
    try:
        # Obtener las credenciales de la variable de entorno FIREBASE_CREDENTIALS_JSON
        firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
        
        if not firebase_creds_json:
            # Si no está la variable de entorno, intentar con el archivo
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            cred_file = os.getenv('FIREBASE_CREDENTIALS', 'pet-plataform-back-firebase-adminsdk-fbsvc-bb8c26602e.json')
            cred_path = os.path.join(base_dir, cred_file)
            
            if not os.path.exists(cred_path):
                raise FileNotFoundError("No se encontró el archivo de credenciales ni la variable FIREBASE_CREDENTIALS_JSON")
                
            # Inicializar con archivo
            cred = credentials.Certificate(cred_path)
        else:
            # Inicializar con variable de entorno
            try:
                cred_info = json.loads(firebase_creds_json)
                cred = credentials.Certificate(cred_info)
            except json.JSONDecodeError:
                # Si el JSON no es válido, intentar como string de ruta
                if os.path.exists(firebase_creds_json):
                    cred = credentials.Certificate(firebase_creds_json)
                else:
                    raise ValueError("FIREBASE_CREDENTIALS_JSON no es un JSON válido ni una ruta de archivo existente")
        
        # Inicializar la aplicación de Firebase si no está ya inicializada
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            current_app.logger.info("Firebase inicializado correctamente")
            
            # Verificar que la conexión con Firestore funciona
            try:
                db = firestore.client()
                db.collection('test').document('connection').set({'status': 'ok'}, merge=True)
                current_app.logger.info("Conexión con Firestore verificada correctamente")
            except Exception as db_error:
                current_app.logger.warning(f"No se pudo verificar la conexión con Firestore: {db_error}")
        
        return True
    except Exception as e:
        current_app.logger.error(f"Error al inicializar Firebase: {e}")
        raise
