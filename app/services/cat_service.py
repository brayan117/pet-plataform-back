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
            return response.json()
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
            Dict[str, Any]: Información de la raza de gato
        """
        try:
            base_url = cls._get_base_url()
            response = requests.get(f"{base_url}breeds/{breed_id}")
            response.raise_for_status()
            return response.json()
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
