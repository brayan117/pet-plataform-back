from flask import Flask
from .dog_routes import dog_bp

def register_routes(app: Flask):
    """
    Registra todas las rutas de la aplicación
    """
    # Registrar rutas de perros
    app.register_blueprint(dog_bp, url_prefix='/api') 