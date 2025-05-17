from flask import jsonify

def register_routes(app):
    """Registra todas las rutas de la aplicación."""
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'success',
            'message': 'Bienvenido a la API de Pet Platform',
            'version': '1.0.0'
        })
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'database': 'connected' if True else 'disconnected'  # Aquí puedes agregar verificaciones reales
        })
