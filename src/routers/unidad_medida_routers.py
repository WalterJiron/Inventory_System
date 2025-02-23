from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.UnidadM_models import(
    UnidadMedida, create_unidadM, update_unidadM
)
from src.controllers.unidad_medida_controllers import UnidadMedidaControllers

unidad_md_router = APIRouter()

@unidad_md_router.get(
        '/unidades_medida', tags=['Unidades de Medida'], response_model=List[UnidadMedida]
)
async def get_unidades_medida():
    """Obtiene todas las unidades de medida activas."""
    try:
        unidades_medida = await UnidadMedidaControllers.get_unidades_medida()
        return unidades_medida
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener unidades de medida: {str(e)}"
        )
    
@unidad_md_router.get(
    '/unidades_medida/{unidad_id}', tags=['Unidades de Medida'], response_model=UnidadMedida
)
async def get_unidad_medida_by_id(unidad_id: int):
    """Obtiene una unidad de medida específica por su ID si está activa."""
    try:
        unidad_medida = await UnidadMedidaControllers.get_unidad_medida_by_id(unidad_id)
        return unidad_medida
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener unidad de medida: {str(e)}"
        )
    
@unidad_md_router.post(
    '/unidades_medida', tags= ['Unidades de Medida'], status_code= status.HTTP_201_CREATED
)
async def create_unidad_medida(unidad_data: create_unidadM):
    """Crea una nueva unidad de medida."""
    try:
        unidad_medida = await UnidadMedidaControllers.create_unidad_medida(unidad_data)
        return unidad_medida
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la unidad de medida: {str(e)}"
        )
    
@unidad_md_router.put( '/unidades_medida/{unidad_id}', tags=['Unidades de Medida'] )
async def update_unidad_medida(unidad_id: int, unidad_data: update_unidadM) -> dict:
    """Actualiza una unidad de medida específica."""
    try:
        unidad_medida = await UnidadMedidaControllers.update_unidad_medida(unidad_id, unidad_data)
        return unidad_medida
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la unidad de medida: {str(e)}"
        )
    
@unidad_md_router.delete( '/unidades_medida/{unidad_id}', tags=['Unidades de Medida'] )
async def delete_unidad_medida(unidad_id: int) -> dict:
    """Elimina una unidad de medida específica."""
    try:
        unidad_medida = await UnidadMedidaControllers.deactivate_unidad_medida(unidad_id)
        return unidad_medida
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la unidad de medida: {str(e)}"
        )