import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import current_app

def init_firebase():
    """Inicializa la aplicación de Firebase con las credenciales."""
    try:
        # Obtener la ruta del archivo de credenciales
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cred_file = os.getenv('FIREBASE_CREDENTIALS', 'pet-plataform-back-firebase-adminsdk-fbsvc-bb8c26602e.json')
        cred_path = os.path.join(base_dir, cred_file)
        
        # Verificar si el archivo de credenciales existe
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"No se encontró el archivo de credenciales en: {cred_path}")
        
        # Inicializar la aplicación de Firebase si no está ya inicializada
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase inicializado correctamente")
            
            # Verificar que la conexión con Firestore funciona
            try:
                db = firestore.client()
                db.collection('test').document('connection').set({'status': 'ok'}, merge=True)
                print("Conexión con Firestore verificada correctamente")
            except Exception as db_error:
                print(f"Advertencia: No se pudo verificar la conexión con Firestore: {db_error}")
        
        return True
        
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")
        raise
