from fastapi import APIRouter, HTTPException, Query
from app.services.dog_service import DogService
from typing import Dict, Any, Optional

class DogController:
    """
    Controlador para manejar las peticiones relacionadas con perros.
    
    Este controlador actúa como intermediario entre las rutas de la API
    y el servicio de perros, manejando la lógica de presentación y
    el formato de las respuestas.
    
    Características:
    - Paginación flexible
    - Límites configurables
    - Manejo de errores robusto
    - Respuestas estandarizadas
    """
    
    def __init__(self):
        """
        Inicializa el controlador con una instancia del servicio de perros.
        Configura las rutas y sus parámetros.
        """
        self.dog_service = DogService()
        self.router = APIRouter(
            prefix="/api/dogs",
            tags=["dogs"],
            responses={
                404: {"description": "Not found"},
                500: {"description": "Internal server error"}
            },
        )
        
        # Registrar rutas con sus configuraciones
        self.router.add_api_route(
            "",
            self.get_dogs,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Obtener lista de perros",
            description="""
            Retorna una lista paginada de razas de perros con sus imágenes.
            
            Parámetros:
            - limit: Número de razas por página (opcional, default: todas)
            - page: Número de página (default: 1)
            
            La respuesta incluye:
            - Lista de perros con sus detalles
            - Metadatos de paginación
            - Total de razas disponibles
            """
        )
        
        self.router.add_api_route(
            "/random-image",
            self.get_random_dog_image,
            methods=["GET"],
            response_model=Dict[str, Any],
            summary="Obtener imagen aleatoria",
            description="""
            Retorna una imagen aleatoria de un perro con información de su raza.
            
            La respuesta incluye:
            - URL de la imagen
            - Detalles de la raza
            - Características físicas
            - Temperamento
            """
        )

    async def get_dogs(
        self,
        limit: Optional[int] = Query(
            default=None,
            description="Número de razas por página. Si no se especifica, retorna todas las razas.",
            ge=1
        ),
        page: int = Query(
            default=1,
            description="Número de página",
            ge=1
        )
    ) -> Dict[str, Any]:
        """
        Endpoint para obtener la lista de perros con sus imágenes.
        
        Este método:
        1. Valida los parámetros de paginación
        2. Llama al servicio para obtener los datos
        3. Formatea la respuesta en un formato estándar
        4. Maneja errores y excepciones
        
        Args:
            limit (Optional[int]): Número de razas por página
            page (int): Número de página
            
        Returns:
            Dict[str, Any]: Respuesta formateada con:
                - Lista de perros
                - Metadatos de paginación
                - Total de razas
                
        Raises:
            HTTPException: Si ocurre un error al obtener los datos
        """
        try:
            # Validar parámetros
            if limit is not None and limit < 1:
                raise HTTPException(
                    status_code=400,
                    detail="El límite debe ser mayor que 0"
                )
            
            if page < 1:
                raise HTTPException(
                    status_code=400,
                    detail="La página debe ser mayor que 0"
                )
            
            # Obtener datos del servicio
            result = self.dog_service.get_dogs(limit=limit, page=page)
            
            # Formatear respuesta
            return {
                'status': 'success',
                'message': 'Lista de perros obtenida exitosamente',
                'data': {
                    'dogs': result['dogs'],
                    'pagination': {
                        'total': result['total'],
                        'page': result['page'],
                        'limit': result['limit'],
                        'total_pages': result['total_pages']
                    }
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener lista de perros: {str(e)}"
            )

    async def get_random_dog_image(self) -> Dict[str, Any]:
        """
        Endpoint para obtener una imagen aleatoria de un perro.
        
        Este método:
        1. Solicita una imagen aleatoria al servicio
        2. Formatea la respuesta con los datos de la imagen y la raza
        3. Maneja casos donde no hay información de raza
        
        Returns:
            Dict[str, Any]: Respuesta formateada con:
                - Datos de la imagen
                - Información de la raza
                - Características físicas
                
        Raises:
            HTTPException: Si ocurre un error al obtener la imagen
        """
        try:
            image_data = self.dog_service.get_random_dog_image()
            return {
                'status': 'success',
                'message': 'Imagen aleatoria obtenida exitosamente',
                'data': image_data
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener imagen aleatoria: {str(e)}"
            ) 