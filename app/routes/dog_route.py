from flask import Blueprint, jsonify, request
from app.services.dog_service import DogService

dog_bp = Blueprint('dog', __name__)

@dog_bp.route('/api/dogs/breeds', methods=['GET'])
def get_all_breeds():
    """
    Obtiene todas las razas de perros
    """
    breeds = DogService.get_all_breeds()
    return jsonify({
        'success': True,
        'message': 'Razas de perros obtenidas correctamente',
        'data': breeds,
        'count': len(breeds)
    }), 200

@dog_bp.route('/api/dogs/breeds-with-images', methods=['GET'])
def get_all_breeds_with_images():
    """
    Obtiene todas las razas de perros con sus imágenes
    """
    breeds = DogService.get_all_breeds_with_images()
    return jsonify({
        'success': True,
        'message': 'Razas de perros con imágenes obtenidas correctamente',
        'data': breeds,
        'count': len(breeds)
    }), 200

@dog_bp.route('/api/dogs/breeds/filter', methods=['GET'])
def filter_breeds():
    """
    Filtra las razas de perros según los criterios especificados.
    
    Parámetros de consulta:
    - size: Tamaño del perro ('small', 'medium', 'large')
    - energy_level: Nivel de energía (1-5)
    - intelligence: Nivel de inteligencia (1-5)
    - breed_group: Grupo de la raza (e.g., 'Working', 'Sporting', etc.)
    - temperament: Temperamento específico a buscar
    """
    # Obtener parámetros de la consulta
    size = request.args.get('size')
    energy_level = request.args.get('energy_level', type=int)
    intelligence = request.args.get('intelligence', type=int)
    breed_group = request.args.get('breed_group')
    temperament = request.args.get('temperament')
    
    # Aplicar filtros
    breeds = DogService.filter_breeds(
        size=size,
        energy_level=energy_level,
        intelligence=intelligence,
        breed_group=breed_group,
        temperament=temperament
    )
    
    return jsonify({
        'success': True,
        'message': 'Razas filtradas correctamente',
        'data': breeds,
        'count': len(breeds),
        'filters_applied': {
            'size': size,
            'energy_level': energy_level,
            'intelligence': intelligence,
            'breed_group': breed_group,
            'temperament': temperament
        }
    }), 200

@dog_bp.route('/api/dogs/breeds/<string:breed_id>', methods=['GET'])
def get_breed(breed_id):
    """
    Obtiene una raza de perro específica por su ID
    """
    breed = DogService.get_breed_by_id(breed_id)
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

@dog_bp.route('/api/dogs/breeds/<string:breed_id>/images', methods=['GET'])
def get_breed_images(breed_id):
    """
    Obtiene imágenes aleatorias de una raza específica.
    
    Este endpoint permite obtener imágenes aleatorias de cualquier raza de perro
    registrada en The Dog API. Las imágenes se obtienen de forma aleatoria cada vez
    que se hace la petición.
    
    Parámetros de consulta:
    - limit: Número máximo de imágenes a obtener (default: 5, max: 10)
    
    Ejemplo de uso:
        GET /api/dogs/breeds/labrador/images?limit=3
    
    Respuesta exitosa (200):
        {
            "success": true,
            "message": "Imágenes de la raza Labrador obtenidas correctamente",
            "data": {
                "breed": {
                    "id": "labrador",
                    "name": "Labrador Retriever",
                    "temperament": "Kind, Outgoing, Agile...",
                    ...
                },
                "images": [
                    {
                        "id": "B1-llgq4m",
                        "url": "https://cdn2.thedogapi.com/images/B1-llgq4m.jpg",
                        "width": 1080,
                        "height": 1080,
                        "breeds": [...]
                    },
                    ...
                ]
            },
            "count": 3
        }
    
    Respuesta de error (404):
        {
            "success": false,
            "message": "Raza no encontrada",
            "data": null
        }
    """
    # Verificar que la raza existe antes de buscar imágenes
    breed = DogService.get_breed_by_id(breed_id)
    if not breed or 'id' not in breed:
        return jsonify({
            'success': False,
            'message': 'Raza no encontrada',
            'data': None
        }), 404
    
    # Obtener y validar el límite de imágenes solicitado
    limit = request.args.get('limit', default=5, type=int)
    if limit < 1 or limit > 10:
        limit = 5  # Limitar a un máximo de 10 imágenes por petición
    
    # Obtener las imágenes aleatorias de la raza
    images = DogService.get_random_images_by_breed(breed_id, limit)
    
    # Devolver la respuesta con la información de la raza y sus imágenes
    return jsonify({
        'success': True,
        'message': f'Imágenes de la raza {breed["name"]} obtenidas correctamente',
        'data': {
            'breed': breed,  # Información completa de la raza
            'images': images  # Lista de imágenes aleatorias
        },
        'count': len(images)  # Número de imágenes obtenidas
    }), 200

@dog_bp.route('/api/dogs/random-image', methods=['GET'])
def get_random_image():
    """
    Obtiene una imagen aleatoria de un perro
    """
    image = DogService.get_random_dog_image()
    if not image:
        return jsonify({
            'success': False,
            'message': 'No se pudo obtener la imagen',
            'data': None
        }), 404
        
    return jsonify({
        'success': True,
        'message': 'Imagen obtenida correctamente',
        'data': image
    }), 200 