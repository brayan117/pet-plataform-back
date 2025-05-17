import os
import requests
from typing import List, Dict, Any
from flask import current_app

class CatService:
    # Usar variable de entorno para la URL base de la API
    BASE_URL = os.getenv('CAT_API_BASE_URL', 'https://api.thecatapi.com/v1/')
    
    @classmethod
    def _get_base_url(cls) -> str:
        """Obtiene la URL base de la API desde las variables de entorno."""
        base_url = os.getenv('CAT_API_BASE_URL')
        if not base_url:
            current_app.logger.warning(
                "CAT_API_BASE_URL no está configurada. Usando valor por defecto."
            )
            return 'https://api.thecatapi.com/v1/'
        return base_url
    
    @classmethod
    def _format_breed_data(cls, breed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formatea los datos de la raza según el formato deseado."""
        return {
            'id': breed_data.get('id', ''),
            'name': breed_data.get('name', ''),
            'temperament': breed_data.get('temperament', ''),
            'life_span': breed_data.get('life_span', ''),
            'origin': breed_data.get('origin', ''),
            'description': breed_data.get('description', ''),
            'weight': breed_data.get('weight', {}),
            'hairless': breed_data.get('hairless', 0),
            'energy_level': breed_data.get('energy_level', 0),
            'intelligence': breed_data.get('intelligence', 0)
        }

    @classmethod
    def get_all_breeds(cls) -> List[Dict[str, Any]]:
        """
        Obtiene todas las razas de gatos de The Cat API.
        
        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios con información de razas de gatos
        """
        try:
            base_url = cls._get_base_url()
            response = requests.get(f"{base_url}breeds")
            response.raise_for_status()  # Lanza una excepción para errores HTTP
            
            # Formatear la respuesta según el formato deseado
            breeds = response.json()
            return [cls._format_breed_data(breed) for breed in breeds]
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error al obtener razas de gatos: {str(e)}")
            return []
    
    @classmethod
    def get_breed_by_id(cls, breed_id: str) -> Dict[str, Any]:
        """
        Obtiene una raza de gato específica por su ID.
        
        Args:
            breed_id (str): El ID de la raza de gato
            
        Returns:
            Dict[str, Any]: Información de la raza de gato en el formato deseado
        """
        try:
            base_url = cls._get_base_url()
            response = requests.get(f"{base_url}breeds/{breed_id}")
            response.raise_for_status()
            
            # Formatear la respuesta según el formato deseado
            breed_data = response.json()
            return cls._format_breed_data(breed_data)
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error al obtener la raza {breed_id}: {str(e)}")
            return {}

# Example usage:
if __name__ == "__main__":
    # Get all breeds
    breeds = CatService.get_all_breeds()
    print(f"Found {len(breeds)} cat breeds")
    
    # Get a specific breed (example with Abyssinian)
    if breeds:
        first_breed = breeds[0]
        breed_details = CatService.get_breed_by_id(first_breed['id'])
        print(f"First breed details: {breed_details}")
