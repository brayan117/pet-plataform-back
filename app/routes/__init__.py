from flask import Blueprint, jsonify
from .cat_route import cat_bp
from .user_route import user_bp
from .dog_route import dog_bp

def register_routes(app):
    """Register all routes with the Flask app."""
    # Register blueprints
    app.register_blueprint(cat_bp, url_prefix='')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(dog_bp, url_prefix='')
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'success',
            'message': 'Bienvenido a la API de Pet Platform',
            'version': '1.0.0',
            'endpoints': {
                'cat_breeds': '/api/cats/breeds',
                'cat_breed_by_id': '/api/cats/breeds/<breed_id>',
                'dog_breeds': '/api/dogs/breeds',
                'dog_breed_by_id': '/api/dogs/breeds/<breed_id>',
                'dog_breeds_with_images': '/api/dogs/breeds-with-images',
                'dog_filter_breeds': '/api/dogs/breeds/filter',
                'dog_breed_images': '/api/dogs/breeds/<breed_id>/images',
                'dog_random_image': '/api/dogs/random-image',
                'users': '/api/users',
                'user_by_id': '/api/users/<user_id>'
            }
        })
