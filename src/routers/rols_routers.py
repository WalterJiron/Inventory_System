from fastapi import APIRouter, HTTPException, status
from typing import List
from src.models.Rol_models import Rol, CreateRol, UpdateRol
from src.controllers.rol_controllers import RolControllers

rol_router = APIRouter()

@rol_router.get("/roles", tags=["Roles"], response_model=List[Rol])
async def get_roles():
    """
    Obtiene todos los roles activos
    """
    try:
        roles = await RolControllers.get_rol()
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener roles: {str(e)}"
        )
    
@rol_router.get("/roles/{id_rol}", tags=["Roles"], response_model=Rol)
async def get_rol(id_rol: int):
    """
    Obtiene un rol por su ID.

    - **id_rol**: El ID del rol a buscar.
    """
    try:
        rol = await RolControllers.get_rol_by_id(id_rol)
        return rol
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener rol: {str(e)}"
        )
    
@rol_router.post("/roles", tags=["Roles"], status_code=status.HTTP_201_CREATED)
async def create_new_rol(rol: CreateRol):
    """
    Crea un nuevo rol.

    - **rol**: Datos del rol a crear.
    """
    try:
        result = await RolControllers.create_rol(rol)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear rol: {str(e)}"
        )
    
@rol_router.put("/roles/{id_rol}", tags=["Roles"])
async def update_rol(id_rol: int, rol: UpdateRol) -> dict:
    """
    Actualiza un rol por su ID.

    - **id_rol**: El ID del rol a actualizar.
    - **rol**: Datos del rol a actualizar.
    """
    try:
        result = await RolControllers.update_rol(id_rol, rol)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar rol: {str(e)}"
        )
    
@rol_router.delete("/roles/{id_rol}", tags=["Roles"])
async def delete_rol(id_rol: int) -> dict:
    """
    Elimina un rol por su ID.

    - **id_rol**: El ID del rol a eliminar.
    """
    try:
        result = await RolControllers.deactivate_rol(id_rol)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar rol: {str(e)}"
        )