from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.MovimientoInv_models import (
    MovimientoInventario,
    CreateMovimientoInventario,
    UpdateMovimientoInventario
)
from src.controllers.movimiento_inventario_controllers import MovimientoInventarioControllers

inven_mov_router = APIRouter()

@inven_mov_router.get(
        "/inventory_movements", tags=["Movimientos de Inventario"], 
        response_model=List[MovimientoInventario]
)
async def get_inventory_movements():
    """
    Obtiene todos los movimientos de inventario
    """
    try:
        inventory_movements = await MovimientoInventarioControllers.get_movimiento_inventario()
        return inventory_movements
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener movimientos de inventario: {str(e)}"
        )
    
@inven_mov_router.get(
        "/inventory_movements/{inventory_movement_id}", tags=["Movimientos de Inventario"], 
        response_model=MovimientoInventario
)
async def get_inventory_movement(inventory_movement_id: int):
    """
    Obtiene un movimiento de inventario por su ID.
    
    - **inventory_movement_id**: El ID del movimiento de inventario a buscar.
    """
    try:
        inventory_movement = await MovimientoInventarioControllers.get_movimiento_inventario_by_id(inventory_movement_id)
        
        # Miramos si la respuesta en un error
        if inventory_movement is MovimientoInventario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movimiento de inventario no encontrado"
            )
        
        return inventory_movement
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener movimiento de inventario: {str(e)}"
        )

@inven_mov_router.post(
        "/inventory_movements", tags=["Movimientos de Inventario"], 
        status_code=status.HTTP_201_CREATED
)
async def create_new_inventory_movement(inventory_movement: CreateMovimientoInventario):
    """
    Crea un nuevo movimiento de inventario.
    
    - **inventory_movement**: Datos del movimiento de inventario a crear.
    """
    try:
        result = await MovimientoInventarioControllers.create_movimiento_inventario(inventory_movement)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear movimiento de inventario: {str(e)}"
        )

@inven_mov_router.put(
        "/inventory_movements/{inventory_movement_id}", tags=["Movimientos de Inventario"], 
        response_model= dict
)
async def update_inventory_movement(inventory_movement_id: int, inventory_movement: UpdateMovimientoInventario):
    """
    Actualiza un movimiento de inventario.
    
    - **inventory_movement_id**: El ID del movimiento de inventario a actualizar.
    - **inventory_movement**: Datos del movimiento de inventario a actualizar.
    """
    try:
        result = await MovimientoInventarioControllers.update_movimiento_inventario(inventory_movement_id, inventory_movement)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movimiento de inventario no encontrado"
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar movimiento de inventario: {str(e)}"
        )

@inven_mov_router.delete(
        "/inventory_movements/{inventory_movement_id}", 
        tags=["Movimientos de Inventario"]
)
async def delete_inventory_movement(inventory_movement_id: int) -> dict:
    """
    Elimina un movimiento de inventario por su ID.
    
    - **inventory_movement_id**: El ID del movimiento de inventario a eliminar.
    """
    try:
        result = await MovimientoInventarioControllers.delete_movimiento_inventario(inventory_movement_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar movimiento de inventario: {str(e)}"
        )