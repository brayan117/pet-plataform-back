from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.services.dog_service import DogService
from app.config.firebase_config import initialize_firebase
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
import logging

# Configuración del sistema de logging
# Se establece el nivel de logging a INFO para ver mensajes informativos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carga de variables de entorno
# Se cargan las variables desde el archivo .env
logger.info("Intentando cargar variables de entorno...")
logger.info(f"Directorio actual: {os.getcwd()}")
load_dotenv()

# Verificación de la API key de The Dog API
# Esta key es necesaria para hacer peticiones a la API
DOG_API_KEY = os.getenv("DOG_API_KEY")
logger.info(f"DOG_API_KEY encontrada: {'Sí' if DOG_API_KEY else 'No'}")
if not DOG_API_KEY:
    logger.error("DOG_API_KEY no está configurada en el archivo .env")
    raise ValueError("DOG_API_KEY no está configurada en el archivo .env")

# Inicialización de Firebase
# Se configura la conexión con Firebase para futuras funcionalidades
try:
    db = initialize_firebase()
    logger.info("Firebase inicializado correctamente")
except Exception as e:
    logger.error(f"Error al inicializar Firebase: {str(e)}")
    raise

# Creación de la aplicación FastAPI
# Se configura con metadatos básicos
app = FastAPI(
    title="Pet Platform API",
    description="API para la plataforma de mascotas",
    version="1.0.0"
)

# Configuración de CORS
# Permite peticiones desde cualquier origen (en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos usando Pydantic
# Estos modelos definen la estructura de los datos que se manejan en la API

class DogImage(BaseModel):
    """Modelo para representar una imagen de perro"""
    id: str
    url: str
    width: Optional[int] = None
    height: Optional[int] = None

class DogWeight(BaseModel):
    """Modelo para representar el peso de un perro en diferentes unidades"""
    imperial: str  # Libras
    metric: str    # Kilogramos

class DogHeight(BaseModel):
    """Modelo para representar la altura de un perro en diferentes unidades"""
    imperial: str  # Pulgadas
    metric: str    # Centímetros

class DogBreed(BaseModel):
    """Modelo para representar una raza de perro con sus características"""
    id: int
    name: str
    description: Optional[str] = None
    temperament: Optional[str] = None
    life_span: Optional[str] = None
    weight: Optional[DogWeight] = None
    height: Optional[DogHeight] = None
    breed_group: Optional[str] = None
    origin: Optional[str] = None
    bred_for: Optional[str] = None

class Dog(BaseModel):
    """Modelo completo para representar un perro con todos sus datos"""
    id: int
    name: str
    description: Optional[str] = None
    temperament: Optional[str] = None
    life_span: Optional[str] = None
    weight: Optional[DogWeight] = None
    height: Optional[DogHeight] = None
    image: Optional[DogImage] = None
    breed_group: Optional[str] = None
    origin: Optional[str] = None
    bred_for: Optional[str] = None
    reference_image_id: Optional[str] = None

class DogResponse(BaseModel):
    """Modelo para la respuesta estándar de la API"""
    status: str
    message: str
    data: dict

class RazaPerro(BaseModel):
    """Modelo en español para representar una raza de perro"""
    id: int
    nombre: str
    descripcion: Optional[str] = None
    temperamento: Optional[str] = None
    vida_promedio: Optional[str] = None
    origen: Optional[str] = None
    imagen: Optional[str] = None

class RazaPerroResponse(BaseModel):
    """Modelo para la respuesta de la lista de razas de perros"""
    razas: List[RazaPerro]

# Instancia del servicio de perros
dog_service = DogService()

@app.get("/razas/perros", response_model=RazaPerroResponse)
async def listar_perros(
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
):
    """
    Endpoint principal para obtener la lista completa de razas de perros.
    
    Este endpoint:
    1. Consulta la API de The Dog API para obtener todas las razas
    2. Aplica paginación si se especifica
    3. Para cada raza, obtiene una imagen aleatoria
    4. Formatea los datos al modelo RazaPerro
    
    Args:
        limit (Optional[int]): Número de razas por página
        page (int): Número de página
        
    Returns:
        RazaPerroResponse: Lista de razas de perros con sus detalles e imágenes
        
    Raises:
        HTTPException: Si ocurre un error al obtener los datos
    """
    try:
        # URL y headers para la petición a la API
        url_razas = "https://api.thedogapi.com/v1/breeds"
        headers = {"x-api-key": DOG_API_KEY}
        
        logger.info("Iniciando petición a la API de perros...")
        logger.info(f"URL: {url_razas}")
        
        # Realizar petición a la API
        r = requests.get(url_razas, headers=headers)
        logger.info(f"Status Code: {r.status_code}")
        
        # Verificar respuesta
        if r.status_code != 200:
            logger.error(f"Error en la respuesta: {r.text}")
            raise HTTPException(status_code=r.status_code, detail="Error al obtener razas de perros")
        
        # Procesar respuesta
        razas = r.json()
        total_razas = len(razas)
        logger.info(f"Se obtuvieron {total_razas} razas")
        
        # Aplicar paginación
        if limit is None:
            limit = total_razas
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        razas_pagina = razas[start_idx:end_idx]
        
        # Procesar cada raza
        resultado = []
        for raza in razas_pagina:
            try:
                breed_id = raza.get("id")
                logger.info(f"Procesando raza ID: {breed_id}, Nombre: {raza.get('name')}")

                # Obtener imagen aleatoria para la raza
                url_img = f"https://api.thedogapi.com/v1/images/search?breed_id={breed_id}&limit=1"
                r_img = requests.get(url_img, headers=headers)
                
                if r_img.status_code != 200:
                    logger.error(f"Error al obtener imagen para raza {breed_id}: {r_img.text}")
                    continue
                
                # Procesar imagen
                img_data = r_img.json()
                img_url = img_data[0]["url"] if img_data else None

                # Crear objeto RazaPerro
                perro = RazaPerro(
                    id=breed_id,
                    nombre=raza.get("name"),
                    descripcion=raza.get("bred_for"),
                    temperamento=raza.get("temperament"),
                    vida_promedio=raza.get("life_span"),
                    origen=raza.get("origin"),
                    imagen=img_url
                )
                resultado.append(perro)
                logger.info(f"Raza {breed_id} procesada exitosamente")
                
            except Exception as e:
                logger.error(f"Error procesando raza {breed_id}: {str(e)}")
                continue

        # Verificar si se encontraron razas
        if not resultado:
            logger.error("No se encontraron razas de perros")
            raise HTTPException(status_code=404, detail="No se encontraron razas de perros")

        logger.info(f"Proceso completado. Se procesaron {len(resultado)} razas exitosamente")
        return RazaPerroResponse(razas=resultado)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en la petición HTTP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al consultar la API de perros: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dogs", response_model=DogResponse)
async def get_dogs(
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
):
    """
    Endpoint alternativo para obtener una lista de perros.
    
    Args:
        limit (Optional[int]): Número de razas por página
        page (int): Número de página
        
    Returns:
        DogResponse: Lista de perros con sus detalles y metadatos de paginación
    """
    try:
        result = dog_service.get_dogs(limit=limit, page=page)
        return {
            "status": "success",
            "message": "Lista de perros obtenida exitosamente",
            "data": {
                "dogs": result["dogs"],
                "pagination": {
                    "total": result["total"],
                    "page": result["page"],
                    "limit": result["limit"],
                    "total_pages": result["total_pages"]
                }
            }
        }
    except Exception as e:
        logger.error(f"Error en get_dogs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dogs/random-image", response_model=DogResponse)
async def get_random_dog_image():
    """
    Endpoint para obtener una imagen aleatoria de un perro.
    
    Returns:
        DogResponse: Datos de la imagen aleatoria y su raza
    """
    try:
        image_data = dog_service.get_random_dog_image()
        return {
            "status": "success",
            "message": "Imagen aleatoria obtenida exitosamente",
            "data": image_data
        }
    except Exception as e:
        logger.error(f"Error en get_random_dog_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 