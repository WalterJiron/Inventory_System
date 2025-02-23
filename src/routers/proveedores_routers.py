from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.Proveedor_models import Proveedor, ProveedorCreate, ProveedorUpdate
from src.controllers.proveedores_controllers import ProveedoresControllers

proveedor_router = APIRouter()

@proveedor_router.get("/proveedores", tags=["Proveedores"], response_model=List[Proveedor])
async def get_proveedores():
    """
    Obtiene todos los proveedores activos
    """
    try:
        proveedores = await ProveedoresControllers.get_proveedores()
        return proveedores
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedores: {str(e)}"
        )
    
@proveedor_router.get("/proveedores/{id_proveedor}", tags=["Proveedores"], response_model=Proveedor)
async def get_proveedor(id_proveedor: int):
    """
    Obtiene un proveedor por su ID.

    - **id_proveedor**: El ID del proveedor a buscar.
    """
    try:
        proveedor = await ProveedoresControllers.get_proveedor_by_id(id_proveedor)
        return proveedor
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}"
        )
    
@proveedor_router.post("/proveedores", tags=["Proveedores"], status_code=status.HTTP_201_CREATED)
async def create_new_proveedor(proveedor: ProveedorCreate):
    """
    Crea un nuevo proveedor.

    - **proveedor**: Datos del proveedor a crear.
    """
    try:
        result = await ProveedoresControllers.create_proveedor(proveedor)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear proveedor: {str(e)}"
        )
    
@proveedor_router.put("/proveedores/{id_proveedor}", tags=["Proveedores"])
async def update_proveedor(id_proveedor: int, proveedor: ProveedorUpdate) -> dict:
    """
    Actualiza un proveedor por su ID.

    - **id_proveedor**: El ID del proveedor a actualizar.
    - **proveedor**: Datos del proveedor a actualizar.
    """
    try:
        result = await ProveedoresControllers.update_proveedor(id_proveedor, proveedor)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar proveedor: {str(e)}"
        )
    
@proveedor_router.delete("/proveedores/{id_proveedor}", tags=["Proveedores"])
async def delete_proveedor(id_proveedor: int) -> dict:
    """
    Elimina un proveedor por su ID.

    - **id_proveedor**: El ID del proveedor a eliminar.
    """
    try:
        result = await ProveedoresControllers.delete_proveedor(id_proveedor)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar proveedor: {str(e)}"
        )