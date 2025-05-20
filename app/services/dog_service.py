import os
import requests
from typing import List, Dict, Any
# from flask import current_app  # No usar logger de Flask fuera de contexto

class DogService:
    # Usar variable de entorno para la URL base de la API
    BASE_URL = os.getenv('DOG_API_BASE_URL', 'https://api.thedogapi.com/v1/')
    
    @classmethod
    def _get_headers(cls) -> Dict[str, str]:
        """Obtiene los headers necesarios para las peticiones a la API."""
        api_key = os.getenv('DOG_API_KEY', 'DEMO-API-KEY')
        return {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
    
    @classmethod
    def _get_base_url(cls) -> str:
        """Obtiene la URL base de la API desde las variables de entorno."""
        base_url = os.getenv('DOG_API_BASE_URL')
        if not base_url:
            print("DOG_API_BASE_URL no está configurada. Usando valor por defecto.")
            return 'https://api.thedogapi.com/v1/'
        return base_url
    
    @classmethod
    def _format_breed_data(cls, breed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formatea los datos de la raza según el formato deseado."""
        reference_image_id = breed_data.get('reference_image_id', '')
        image_url = f"https://cdn2.thedogapi.com/images/{reference_image_id}.jpg" if reference_image_id else ''
        
        return {
            'id': breed_data.get('id', ''),
            'name': breed_data.get('name', ''),
            'temperament': breed_data.get('temperament', ''),
            'life_span': breed_data.get('life_span', ''),
            'origin': breed_data.get('origin', ''),
            'description': breed_data.get('description', ''),
            'weight': breed_data.get('weight', {}),
            'height': breed_data.get('height', {}),
            'bred_for': breed_data.get('bred_for', ''),
            'breed_group': breed_data.get('breed_group', ''),
            'energy_level': breed_data.get('energy_level', 0),
            'intelligence': breed_data.get('intelligence', 0),
            'reference_image_id': reference_image_id,
            'image_url': image_url
        }

    @classmethod
    def filter_breeds(cls, 
                     size: str = None,
                     energy_level: int = None,
                     intelligence: int = None,
                     breed_group: str = None,
                     temperament: str = None) -> List[Dict[str, Any]]:
        """
        Filtra las razas de perros según los criterios especificados.
        
        Args:
            size (str): Tamaño del perro ('small', 'medium', 'large')
            energy_level (int): Nivel de energía (1-5)
            intelligence (int): Nivel de inteligencia (1-5)
            breed_group (str): Grupo de la raza (e.g., 'Working', 'Sporting', etc.)
            temperament (str): Temperamento específico a buscar
            
        Returns:
            List[Dict[str, Any]]: Lista de razas que cumplen con los criterios
        """
        breeds = cls.get_all_breeds()
        filtered_breeds = breeds.copy()
        
        if size:
            filtered_breeds = [
                breed for breed in filtered_breeds
                if cls._get_size_category(breed.get('weight', {})) == size.lower()
            ]
            
        if energy_level is not None:
            filtered_breeds = [
                breed for breed in filtered_breeds
                if breed.get('energy_level', 0) == energy_level
            ]
            
        if intelligence is not None:
            filtered_breeds = [
                breed for breed in filtered_breeds
                if breed.get('intelligence', 0) == intelligence
            ]
            
        if breed_group:
            filtered_breeds = [
                breed for breed in filtered_breeds
                if breed.get('breed_group', '').lower() == breed_group.lower()
            ]
            
        if temperament:
            filtered_breeds = [
                breed for breed in filtered_breeds
                if temperament.lower() in breed.get('temperament', '').lower()
            ]
            
        return filtered_breeds

    @classmethod
    def _get_size_category(cls, weight: Dict[str, str]) -> str:
        """
        Determina la categoría de tamaño basada en el peso.
        
        Args:
            weight (Dict[str, str]): Diccionario con peso en imperial y metric
            
        Returns:
            str: 'small', 'medium', o 'large'
        """
        try:
            # Intentar obtener el peso en kg
            if 'metric' in weight:
                weight_str = weight['metric'].split('-')[0].strip()
                weight_kg = float(weight_str)
            else:
                # Si no hay peso en kg, convertir de libras
                weight_str = weight['imperial'].split('-')[0].strip()
                weight_lbs = float(weight_str)
                weight_kg = weight_lbs * 0.453592
            
            if weight_kg < 10:
                return 'small'
            elif weight_kg < 25:
                return 'medium'
            else:
                return 'large'
        except (ValueError, KeyError, IndexError):
            return 'medium'  # Valor por defecto si no se puede determinar

    @classmethod
    def get_dog_image(cls, reference_image_id: str) -> Dict[str, Any]:
        if not reference_image_id:
            return {}
        try:
            base_url = cls._get_base_url()
            headers = cls._get_headers()
            response = requests.get(f"{base_url}images/{reference_image_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la imagen del perro: {str(e)}")
            return {}

    @classmethod
    def get_all_breeds_with_images(cls) -> List[Dict[str, Any]]:
        breeds = cls.get_all_breeds()
        for breed in breeds:
            if 'reference_image_id' in breed and breed['reference_image_id']:
                try:
                    image_data = cls.get_dog_image(breed['reference_image_id'])
                    breed['image_url'] = image_data.get('url', '')
                except Exception as e:
                    print(f"Error al obtener la imagen para la raza {breed.get('id', 'unknown')}: {str(e)}")
                    breed['image_url'] = ''
            else:
                breed['image_url'] = ''
        return breeds

    @classmethod
    def get_all_breeds(cls) -> List[Dict[str, Any]]:
        """
        Obtiene todas las razas de perros de The Dog API.
        
        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios con información de razas de perros
        """
        try:
            base_url = cls._get_base_url()
            headers = cls._get_headers()
            response = requests.get(f"{base_url}breeds", headers=headers)
            response.raise_for_status()
            
            breeds = response.json()
            return [cls._format_breed_data(breed) for breed in breeds]
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener razas de perros: {str(e)}")
            return []
    
    @classmethod
    def get_breed_by_id(cls, breed_id: str) -> Dict[str, Any]:
        """
        Obtiene una raza de perro específica por su ID.
        
        Args:
            breed_id (str): El ID de la raza de perro
            
        Returns:
            Dict[str, Any]: Información de la raza de perro en el formato deseado
        """
        try:
            base_url = cls._get_base_url()
            headers = cls._get_headers()
            response = requests.get(f"{base_url}breeds/{breed_id}", headers=headers)
            response.raise_for_status()
            
            breed_data = response.json()
            return cls._format_breed_data(breed_data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la raza {breed_id}: {str(e)}")
            return {}

    @classmethod
    def get_random_dog_image(cls) -> Dict[str, Any]:
        """
        Obtiene una imagen aleatoria de un perro.
        
        Returns:
            Dict[str, Any]: Un diccionario con la información de la imagen o un diccionario vacío en caso de error
        """
        try:
            base_url = cls._get_base_url()
            headers = cls._get_headers()
            response = requests.get(
                f"{base_url}images/search",
                headers=headers,
                params={
                    'size': 'med',
                    'mime_types': 'jpg',
                    'format': 'json',
                    'has_breeds': 'true',
                    'order': 'RANDOM',
                    'page': 0,
                    'limit': 1
                }
            )
            response.raise_for_status()
            data = response.json()
            return data[0] if data else {}
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la imagen aleatoria del perro: {str(e)}")
            return {}

    @classmethod
    def get_random_images_by_breed(cls, breed_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene imágenes aleatorias de una raza específica.
        
        Este método hace una petición a The Dog API para obtener imágenes aleatorias
        de una raza específica. Las imágenes se obtienen de forma aleatoria cada vez
        que se llama al método.
        
        Args:
            breed_id (str): ID de la raza (ej: 'labrador', 'husky', 'affenpinscher')
            limit (int): Número máximo de imágenes a obtener (default: 5, max: 10)
            
        Returns:
            List[Dict[str, Any]]: Lista de imágenes con la siguiente estructura:
                {
                    'id': str,           # ID único de la imagen
                    'url': str,          # URL directa a la imagen
                    'width': int,        # Ancho de la imagen en píxeles
                    'height': int,       # Alto de la imagen en píxeles
                    'breeds': [          # Información de la raza en la imagen
                        {
                            'id': str,
                            'name': str,
                            'temperament': str,
                            ...
                        }
                    ]
                }
        """
        try:
            # Construir la URL base y headers para la petición
            base_url = cls._get_base_url()
            headers = cls._get_headers()
            
            # Obtener más imágenes de las necesarias para asegurar aleatoriedad
            response = requests.get(
                f"{base_url}images/search",
                headers=headers,
                params={
                    'size': 'med',           # Tamaño de imagen: med (medio)
                    'mime_types': 'jpg',     # Formato de imagen: JPG
                    'format': 'json',        # Formato de respuesta: JSON
                    'has_breeds': 'true',    # Incluir información de la raza
                    'breed_id': breed_id,    # ID de la raza específica
                    'order': 'RANDOM',       # Orden aleatorio de las imágenes
                    'page': 0,               # Primera página de resultados
                    'limit': limit * 2       # Pedir el doble de imágenes para tener más opciones
                }
            )
            
            # Verificar si la petición fue exitosa
            response.raise_for_status()
            
            # Obtener todas las imágenes
            all_images = response.json()
            
            # Si no hay suficientes imágenes, devolver las que hay
            if len(all_images) <= limit:
                return all_images
            
            # Seleccionar aleatoriamente 'limit' imágenes del conjunto
            import random
            random.shuffle(all_images)
            return all_images[:limit]
            
        except requests.exceptions.RequestException as e:
            # Manejar errores de la petición (red, API, etc.)
            print(f"Error al obtener imágenes aleatorias de la raza {breed_id}: {str(e)}")
            return [] 