from fastapi import APIRouter, Query
from app.controllers.dog_controller import DogController
from typing import Dict, Any

# Crear instancia del controlador
dog_controller = DogController()

# Crear router para las rutas de perros
router = APIRouter(
    prefix="/api",
    tags=["dogs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/dogs", response_model=Dict[str, Any])
async def get_dogs(limit: int = Query(default=10, description="Número máximo de perros a retornar")):
    """
    Endpoint para obtener la lista de perros con sus imágenes.
    Este endpoint permite obtener una lista paginada de razas de perros,
    cada una con su imagen representativa y detalles completos.
    Args:
        limit (int): Número máximo de perros a retornar (default: 10)
    Returns:
        Dict[str, Any]: Respuesta con la lista de perros y metadatos
    Raises:
        HTTPException: Si ocurre un error al obtener los datos
    """
    return await dog_controller.get_dogs(limit)

@router.get("/dogs/random-image", response_model=Dict[str, Any])
async def get_random_dog_image():
    """
    Endpoint para obtener una imagen aleatoria de un perro.
    Este endpoint retorna una imagen aleatoria de un perro junto con
    la información detallada de su raza, incluyendo características
    físicas y temperamento.
    Returns:
        Dict[str, Any]: Respuesta con la imagen aleatoria y datos de la raza
    Raises:
        HTTPException: Si ocurre un error al obtener la imagen
    """
    return await dog_controller.get_random_dog_image() 