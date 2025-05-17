from app.services.firebase_service import db
from flask import current_app

def get_users():
    """
    Obtiene todos los usuarios de Firestore.
    
    Returns:
        tuple: (lista_de_usuarios, código_de_estado)
    """
    if db is None:
        current_app.logger.error("Firebase no está inicializado")
        return [], 500
        
    try:
        users_ref = db.collection('users')
        users = users_ref.stream()
        
        # Convertir los documentos a diccionarios
        users_list = [{"id": user.id, **user.to_dict()} for user in users]
        
        return users_list, 200
    except Exception as e:
        current_app.logger.error(f"Error al obtener usuarios: {str(e)}")
        return [], 500
