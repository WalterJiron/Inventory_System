from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.UbicacionAlm_models import(
    UbicacionAlmacen, UbicacionAlmacenCreate, UbicacionAlmacenUpdate
)
from src.controllers.ubicacion_almacen_controllers import UbicacionesAlmacenController

ubicacion_alm_router = APIRouter()

@ubicacion_alm_router.get(
        '/ubicaciones', tags=['Ubicaciones de Almacen'], response_model=List[UbicacionAlmacen]
)
async def get_ubicaciones():
    """Obtiene todas las ubicaciones activas del almacen."""
    try:
        ubicaciones = await UbicacionesAlmacenController.get_ubicaciones()
        return ubicaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones: {str(e)}"
        )
    
@ubicacion_alm_router.get(
    '/ubicaciones/{ubicacion_id}', tags=['Ubicaciones de Almacen'], response_model=UbicacionAlmacen
)
async def get_ubicacion_by_id(ubicacion_id: int):
    """Obtiene una ubicación específica por su ID si está activa."""
    try:
        ubicacion = await UbicacionesAlmacenController.get_ubicacion_by_id(ubicacion_id)
        return ubicacion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicación: {str(e)}"
        )
    
@ubicacion_alm_router.post(
    '/ubicaciones', tags=['Ubicaciones de Almacen'], status_code=status.HTTP_201_CREATED
)
async def create_ubicacion(ubicacion_data: UbicacionAlmacenCreate):
    """Crea una nueva ubicación en el almacen."""
    try:
        ubicacion = await UbicacionesAlmacenController.create_ubicacion(ubicacion_data)
        return ubicacion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la ubicación: {str(e)}"
        )
    
@ubicacion_alm_router.put( '/ubicaciones/{ubicacion_id}', tags=['Ubicaciones de Almacen'] )
async def update_ubicacion(ubicacion_id: int, ubicacion_data: UbicacionAlmacenUpdate) -> dict:
    """Actualiza una ubicación específica del almacen."""
    try:
        ubicacion = await UbicacionesAlmacenController.update_ubicacion(ubicacion_id, ubicacion_data)
        return ubicacion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la ubicación: {str(e)}"
        )
    
@ubicacion_alm_router.delete( '/ubicaciones/{ubicacion_id}', tags=['Ubicaciones de Almacen'] )
async def delete_ubicacion(ubicacion_id: int) -> dict:
    """Elimina una ubicación específica del almacen."""
    try:
        result = await UbicacionesAlmacenController.delete_ubicacion(ubicacion_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la ubicación: {str(e)}"
        )