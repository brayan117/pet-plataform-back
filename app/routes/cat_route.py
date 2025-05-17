from flask import Blueprint, jsonify
from app.services.cat_service import CatService

cat_bp = Blueprint('cat', __name__)

@cat_bp.route('/api/cats/breeds', methods=['GET'])
def get_all_breeds():
    """
    Endpoint to get all cat breeds
    """
    breeds = CatService.get_all_breeds()
    return jsonify({
        'success': True,
        'data': breeds,
        'count': len(breeds)
    }), 200

@cat_bp.route('/api/cats/breeds/<string:breed_id>', methods=['GET'])
def get_breed(breed_id):
    """
    Endpoint to get a specific cat breed by ID
    """
    breed = CatService.get_breed_by_id(breed_id)
    if not breed:
        return jsonify({
            'success': False,
            'message': 'Breed not found'
        }), 404
        
    return jsonify({
        'success': True,
        'data': breed
    }), 200
