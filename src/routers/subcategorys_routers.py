from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.Subcategoria_models import (
    Subcategoria, CreateSubCategoria, UpdateSubCategoria
)
from src.controllers.subcategoria_controllers import SubcategoriaControllers

subcat_router = APIRouter()

@subcat_router.get("/subcategorias", tags=["Subcategorias"], response_model=List[Subcategoria])
async def get_subcategorias():
    """
    Obtiene todas las subcategorías activas.
    """
    try:
        subcategorias = await SubcategoriaControllers.get_subcategorias()
        return subcategorias
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener subcategorías: {str(e)}"
        )
    
@subcat_router.get("/subcategorias/{id_subcat}", tags=["Subcategorias"], response_model=Subcategoria)
async def get_subcategoria(id_subcat: int):
    """
    Obtiene una subcategoría por su ID.
    
    - **id_subcat**: El ID de la subcategoría a buscar.
    """
    try:
        subcategoria = await SubcategoriaControllers.get_subcategoria_by_id(id_subcat)
        return subcategoria
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener subcategoría: {str(e)}"
        )
    
@subcat_router.post("/subcategorias", tags=["Subcategorias"], status_code=status.HTTP_201_CREATED)
async def create_subcategoria(subcategoria: CreateSubCategoria):
    """
    Crea una nueva subcategoría.
    
    - **subcategoria**: Datos de la subcategoría a crear.
    """
    try:
        result = await SubcategoriaControllers.create_subcategoria(subcategoria)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear subcategoría: {str(e)}"
        )
    
@subcat_router.put("/subcategorias/{id_subcat}", tags=["Subcategorias"])
async def update_subcategoria(id_subcat: int, subcategoria: UpdateSubCategoria):
    """
    Actualiza una subcategoría.
    
    - **id_subcat**: El ID de la subcategoría a actualizar.
    - **subcategoria**: Datos de la subcategoría a actualizar.
    """
    try:
        result = await SubcategoriaControllers.update_subcategoria(id_subcat, subcategoria)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar subcategoría: {str(e)}"
        )
    
@subcat_router.delete("/subcategorias/{id_subcat}", tags=["Subcategorias"])
async def delete_subcategoria(id_subcat: int):
    """
    Elimina una subcategoría.
    
    - **id_subcat**: El ID de la subcategoría a eliminar.
    """
    try:
        result = await SubcategoriaControllers.deactivate_subcategoria(id_subcat)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar subcategoría: {str(e)}"
        )