from typing import List
from fastapi import APIRouter, HTTPException, status
from src.models.Almacen_models import Almacen, AlmacenCreate, AlmacenUpdate
from src.controllers.almacen_controller import AlmacenesControllers

almacen_router = APIRouter()

@almacen_router.get('/almacen', tags=['Almacenes'], response_model= List[Almacen])
async def get_almacenes():
    try:
        almacenes = await AlmacenesControllers.get_almacenes()
        return almacenes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error al obtener almacenes: {e}'    
        )

@almacen_router.get('/almacen/{id_almacen}', tags=['Almacenes'], response_model= List[Almacen])
async def get_almacen(id_almacen: int):
    try:
        almacen = await AlmacenesControllers.get_almacen_by_id(id_almacen)
        return almacen
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'Error al obtener almacen: {e}'
        )
    
@almacen_router.post('/almacen', tags=['Almacenes'], status_code= status.HTTP_201_CREATED)
async def almacen_create(almacen: AlmacenCreate):
    try:
        almacen_create = await AlmacenesControllers.almacen_create(almacen)
        return almacen_create
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al crear un almacen: {e}'
        )
    
@almacen_router.put('/almacen/{id_almacen}', tags=['Almacenes'])
async def almacen_update(id_almacen: int, almacen: AlmacenUpdate)  -> dict:
    try:
        result = await AlmacenesControllers.almacen_update(id_almacen, almacen)
        return result
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al actualizar el almacen: {e}'
        )
        
@almacen_router.delete('/almacen/{id_almacen}', tags=['Almacenes'])
async def almacen_delete(id_almacen: int):
    try:
        result = await AlmacenesControllers.delete_almacen(id_almacen)
        return result
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al eliminar el almacen: {e}'
        )