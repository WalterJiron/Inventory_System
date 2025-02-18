from typing import List
from fastapi import APIRouter, HTTPException, status
from src.models.Users_models import UserCreate, UserUpdate, Users  # modelos de usuario
from src.controllers.users_controllers import UsersControllers

# Crear un enrutador para manejar las rutas de usuarios
user_router = APIRouter()

# Ruta para obtener todos los usuarios
@user_router.get("/users", tags=["users"], response_model=List[Users])
async def get_users():
    """
    Obtiene todos los usuarios activos
    """
    try:
        users = await UsersControllers.get_users()  # Llamar a la funcin para obtener usuarios
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}"
        )

# Ruta para obtener un usuario por su IdUser
@user_router.get("/users/{id_user}", tags=["users"], response_model=Users)
async def get_user(id_user: int):
    """
    Obtiene un usuario por su ID.

    - **id_user**: El ID del usuario a buscar.
    """
    try:
        user = await UsersControllers.get_user_by_id(id_user)  # Llamar a la funcion para obtener un usuario por ID
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}"
        )

# Ruta para crear un nuevo usuario
@user_router.post("/users", tags=["users"], status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate):
    """
    Crea un nuevo usuario.

    - **user**: Datos del usuario a crear.
    """
    try:
        result = await UsersControllers.create_user(user)  # Llamar a la funcion para crear un usuario
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear usuario: {str(e)}"
        )

# Ruta para actualizar un usuario existente
@user_router.put("/users/{id_user}", tags=["users"])
async def update_existing_user(id_user: int, user: UserUpdate) -> dict:
    """
    Actualiza un usuario existente.

    - **id_user**: El ID del usuario a actualizar.
    - **user**: Datos del usuario a actualizar.
    """
    try:
        result = await UsersControllers.update_user(id_user, user)  # Llamar a la funcion para actualizar un usuario
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar usuario: {str(e)}"
        )
    
@user_router.delete("/users/{id_user}", tags=['users'])
async def delete_user(id_user: int) -> dict:
    """Elimina un usuario existente mediante su ID."""
    try:
        result = await UsersControllers.delete_users(id_user)
        return result
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f'Error al eliminar usuario: {str(e)}'
        )