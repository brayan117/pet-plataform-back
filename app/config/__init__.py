import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base de la aplicación."""
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-predeterminada')
    
    # Configuración de Firebase
    FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS', 'pet-plataform-back-firebase-adminsdk-fbsvc-bb8c26602e.json')
    
    # Otros ajustes de configuración pueden ir aquí

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
