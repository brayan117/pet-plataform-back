from flask import Blueprint, jsonify
from app.services.cat_service import CatService

cat_bp = Blueprint('cat', __name__)

@cat_bp.route('/api/cats/breeds', methods=['GET'])
def get_all_breeds():
    """
    Obtiene todas las razas de gatos
    """
    breeds = CatService.get_all_breeds()
    return jsonify({
        'success': True,
        'message': 'Razas de gatos obtenidas correctamente',
        'data': breeds,
        'count': len(breeds)
    }), 200

@cat_bp.route('/api/cats/breeds/<string:breed_id>', methods=['GET'])
def get_breed(breed_id):
    """
    Obtiene una raza de gato específica por su ID
    """
    breed = CatService.get_breed_by_id(breed_id)
    if not breed or 'id' not in breed:
        return jsonify({
            'success': False,
            'message': 'Raza no encontrada',
            'data': None
        }), 404
        
    return jsonify({
        'success': True,
        'message': 'Raza obtenida correctamente',
        'data': breed
    }), 200
