from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.Transferencia_models import(
    Transferencia, TransferenciaCreate, TransferenciaUpdate
)
from src.controllers.transferencia_controllers import TransferenciasControllers

transferencia_router = APIRouter()

@transferencia_router.get('/transferencias', tags=['Transferencias'], response_model=List[Transferencia])
async def get_transferencias():
    """Obtiene todas las transferencias de la base de datos."""
    try:
        return await TransferenciasControllers.get_transferencias()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@transferencia_router.get('/transferencias/{id_trasFe}', tags=['Transferencias'], response_model=Transferencia)
async def get_transferencia_by_id(id_trasFe: int):
    """Obtiene una transferencia por su ID."""
    try:
        transferencia = await TransferenciasControllers.get_transferencia_by_id(id_trasFe)
        return transferencia
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@transferencia_router.post('/transferencias', tags=['Transferencias'], status_code= status.HTTP_201_CREATED)
async def create_transferencia(transferencia: TransferenciaCreate):
    """Crea una nueva transferencia."""
    try:
        result = await TransferenciasControllers.create_transferencia(transferencia)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@transferencia_router.put('/transferencias/{id_trasFe}', tags=['Transferencias'])
async def update_transferencia(id_trasFe: int, transferencia: TransferenciaUpdate) -> dict:
    """Actualiza una transferencia existente."""
    try:
        result = await TransferenciasControllers.update_transferencia(id_trasFe, transferencia)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@transferencia_router.delete('/transferencias/{id_trasFe}', tags=['Transferencias'])
async def delete_transferencia(id_trasFe: int) -> dict:
    """Elimina una transferencia de la base de datos."""
    try:
        return await TransferenciasControllers.delete_transferencia(id_trasFe)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )