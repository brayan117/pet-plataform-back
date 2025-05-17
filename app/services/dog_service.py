import requests
from app.config import Config
from typing import List, Dict, Any, Optional

class DogService:
    """
    Servicio para interactuar con The Dog API.
    
    Este servicio proporciona métodos para obtener información sobre razas de perros
    y sus imágenes desde The Dog API. Maneja la autenticación y el formateo de datos.
    
    Características:
    - Paginación de resultados
    - Límites configurables
    - Manejo de errores robusto
    - Caché de datos para optimizar rendimiento
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la configuración base de la API.
        
        Configura:
        - URL base de la API
        - Headers de autenticación con la API key
        - Caché para almacenar datos frecuentemente usados
        """
        self.base_url = Config.DOG_API_BASE_URL
        self.headers = {
            'x-api-key': Config.DOG_API_KEY
        }
        self._breeds_cache = None  # Caché para la lista de razas

    def _get_all_breeds(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las razas de perros disponibles.
        
        Utiliza caché para evitar llamadas innecesarias a la API.
        
        Returns:
            List[Dict[str, Any]]: Lista completa de razas disponibles
            
        Raises:
            Exception: Si hay error al obtener las razas
        """
        if self._breeds_cache is None:
            try:
                response = requests.get(
                    f"{self.base_url}/breeds",
                    headers=self.headers
                )
                response.raise_for_status()
                self._breeds_cache = response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error al obtener razas de perros: {str(e)}")
        return self._breeds_cache

    def get_dogs(self, limit: Optional[int] = None, page: int = 1) -> Dict[str, Any]:
        """
        Obtiene una lista de perros con sus imágenes aleatorias.
        
        Este método:
        1. Obtiene la lista completa de razas (usando caché)
        2. Aplica paginación si se especifica
        3. Para cada raza seleccionada, obtiene una imagen aleatoria
        4. Estructura los datos en un formato consistente
        
        Args:
            limit (Optional[int]): Número máximo de razas a retornar. Si es None, retorna todas.
            page (int): Número de página para paginación (default: 1)
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - dogs: Lista de perros con sus datos
                - total: Total de razas disponibles
                - page: Página actual
                - limit: Límite por página
                - total_pages: Total de páginas
                
        Raises:
            Exception: Si hay error al obtener datos de la API
        """
        try:
            # Obtener todas las razas (usando caché)
            all_breeds = self._get_all_breeds()
            total_breeds = len(all_breeds)
            
            # Calcular paginación
            if limit is None:
                limit = total_breeds
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            
            # Obtener subconjunto de razas según paginación
            breeds_page = all_breeds[start_idx:end_idx]
            
            # Obtener imágenes aleatorias para cada raza
            dogs_with_images = []
            for breed in breeds_page:
                try:
                    # Obtener una imagen aleatoria para esta raza
                    image_response = requests.get(
                        f"{self.base_url}/images/search",
                        params={
                            'breed_id': breed['id'],
                            'limit': 1,
                            'order': 'RANDOM'
                        },
                        headers=self.headers
                    )
                    image_response.raise_for_status()
                    images = image_response.json()

                    # Estructurar la información del perro
                    dog_data = {
                        'id': breed['id'],
                        'name': breed['name'],
                        'description': breed.get('description', ''),
                        'temperament': breed.get('temperament', ''),
                        'life_span': breed.get('life_span', ''),
                        'weight': {
                            'imperial': breed.get('weight', {}).get('imperial', ''),
                            'metric': breed.get('weight', {}).get('metric', '')
                        },
                        'height': {
                            'imperial': breed.get('height', {}).get('imperial', ''),
                            'metric': breed.get('height', {}).get('metric', '')
                        },
                        'image': {
                            'id': images[0]['id'] if images else None,
                            'url': images[0]['url'] if images else None,
                            'width': images[0].get('width', ''),
                            'height': images[0].get('height', '')
                        },
                        'breed_group': breed.get('breed_group', ''),
                        'origin': breed.get('origin', ''),
                        'bred_for': breed.get('bred_for', ''),
                        'reference_image_id': breed.get('reference_image_id', '')
                    }
                    dogs_with_images.append(dog_data)
                except Exception as e:
                    print(f"Error al obtener imagen para la raza {breed['name']}: {str(e)}")
                    continue

            if not dogs_with_images:
                raise Exception("No se pudieron obtener datos de perros")

            # Calcular total de páginas
            total_pages = (total_breeds + limit - 1) // limit

            return {
                'dogs': dogs_with_images,
                'total': total_breeds,
                'page': page,
                'limit': limit,
                'total_pages': total_pages
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener datos de The Dog API: {str(e)}")

    def get_random_dog_image(self) -> Dict[str, Any]:
        """
        Obtiene una imagen aleatoria de un perro con información completa.
        
        Este método:
        1. Solicita una imagen aleatoria que incluya información de la raza
        2. Procesa y estructura los datos de la imagen y la raza
        3. Maneja casos donde la imagen no tiene información de raza
        
        Returns:
            dict: Diccionario con información de la imagen y la raza del perro
            
        Raises:
            Exception: Si hay error al obtener la imagen aleatoria
        """
        try:
            # Solicitar imagen aleatoria con información de raza
            response = requests.get(
                f"{self.base_url}/images/search",
                params={
                    'limit': 1,
                    'order': 'RANDOM',
                    'has_breeds': True  # Asegura que la imagen tenga información de raza
                },
                headers=self.headers
            )
            response.raise_for_status()
            image_data = response.json()[0]
            
            # Procesar información de la raza si está disponible
            if 'breeds' in image_data and image_data['breeds']:
                breed = image_data['breeds'][0]
                return {
                    'image': {
                        'id': image_data['id'],
                        'url': image_data['url'],
                        'width': image_data.get('width', ''),
                        'height': image_data.get('height', '')
                    },
                    'breed': {
                        'id': breed['id'],
                        'name': breed['name'],
                        'description': breed.get('description', ''),
                        'temperament': breed.get('temperament', ''),
                        'life_span': breed.get('life_span', ''),
                        'weight': {
                            'imperial': breed.get('weight', {}).get('imperial', ''),
                            'metric': breed.get('weight', {}).get('metric', '')
                        },
                        'height': {
                            'imperial': breed.get('height', {}).get('imperial', ''),
                            'metric': breed.get('height', {}).get('metric', '')
                        },
                        'breed_group': breed.get('breed_group', ''),
                        'origin': breed.get('origin', ''),
                        'bred_for': breed.get('bred_for', '')
                    }
                }
            
            # Si no hay información de raza, retornar solo datos de la imagen
            return {
                'image': {
                    'id': image_data['id'],
                    'url': image_data['url'],
                    'width': image_data.get('width', ''),
                    'height': image_data.get('height', '')
                }
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener imagen aleatoria: {str(e)}") 