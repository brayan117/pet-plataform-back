from flask import Blueprint, jsonify
from app.controllers.user_controller import get_users

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users, status_code = get_users()
    return jsonify({
        'status': 'success',
        'message': 'Lista de usuarios obtenida correctamente',
        'data': users
    }), status_code

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({
        'status': 'success',
        'message': f'Detalles del usuario {user_id}',
        'data': {'id': user_id}
    })
