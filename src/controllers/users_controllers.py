from src.models.Users_models import Users, UserCreate, UserUpdate
from src.DB import get_connection
from typing import List, Optional
import pyodbc

def _convert_to_user(user_data: tuple) -> Users:
    """Convierte una tupla de datos de la base de datos en un objeto Users."""
    return Users(
        id_user=user_data[0],
        name_user=user_data[1],
        rol_name=user_data[2],
        creation_date=user_data[3],
    )

def get_users() -> List[Users]:
    """Obtiene todos los usuarios activos de la base de datos."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                # Consulta SQL para obtener todos los usuarios activos
                query = """
                    SELECT US.IdUser, US.NameUser, ROL.NameRol, US.CreationDateUser 
                    FROM Usuarios AS US 
                    JOIN Roles AS ROL ON US.RolID = ROL.RolID
                    WHERE US.EstadoUser = 1
                """
                cursor.execute(query)
                users = cursor.fetchall()
                
                # Convertir los resultados en objetos Users
                return [_convert_to_user(user) for user in users]
                
    except pyodbc.Error as e:
        raise Exception(f"Error al obtener usuarios: {str(e)}")
    
def get_user_by_id(id_user: int) -> Optional[Users]:
    """Obtiene un usuario por su ID si está activo."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                # Consulta SQL para obtener un usuario por su IdUser
                query = """
                    SELECT US.IdUser, US.NameUser, ROL.NameRol, US.CreationDateUser 
                    FROM Usuarios AS US 
                    JOIN Roles AS ROL ON US.RolID = ROL.RolID
                    WHERE US.EstadoUser = 1 AND IdUser = ?
                """
                cursor.execute(query, (id_user,))
                user = cursor.fetchone()
                
                if user is None:
                    return None
                
                # Convertir el resultado en un objeto Users
                return _convert_to_user(user)
                
    except pyodbc.Error as e:
        raise Exception(f"Error al obtener usuario por ID: {str(e)}")
    
def create_user(user: UserCreate) -> dict:
    """Crea un nuevo usuario en la base de datos."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                # Consulta SQL para insertar un nuevo usuario
                query = """
                    INSERT INTO Usuarios (NameUser, Clave, RolID)
                    VALUES (?, ?, ?);
                    SELECT SCOPE_IDENTITY() AS IdUser;
                """
                
                # Ejecutar la consulta con los valores del nuevo usuario
                cursor.execute(query, (user.NameUser, user.Clave, user.RolID))
                
                # Obtener el ID del usuario recién creado
                id_user = cursor.fetchone()[0]
                
                connection.commit()
                return {"message": "Usuario creado exitosamente", "id_user": id_user}
                
    except pyodbc.Error as e:
        raise Exception(f"Error al crear usuario: {str(e)}")
    
def update_user(id_user: int, user: UserUpdate) -> dict:
    """Actualiza un usuario existente en la base de datos."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                # Verificar si el usuario existe y está activo
                check_query = """
                    SELECT EstadoUser 
                    FROM Usuarios 
                    WHERE IdUser = ? AND EstadoUser = 1
                """
                cursor.execute(check_query, (id_user,))
                result = cursor.fetchone()
                
                if not result:
                    raise Exception("Usuario no encontrado o inactivo")
                
                # Construir la consulta UPDATE dinámicamente
                update_parts = []
                params = []
                
                if user.NameUser is not None:
                    update_parts.append("NameUser = ?")
                    params.append(user.NameUser)
                    
                if user.Clave is not None:
                    update_parts.append("Clave = ?")
                    params.append(user.Clave)
                    
                if user.RolID is not None:
                    update_parts.append("RolID = ?")
                    params.append(user.RolID)
                    
                if not update_parts:
                    raise Exception("No se proporcionaron campos para actualizar")
                
                # Agregar el ID del usuario a los parámetros
                params.append(id_user)
                
                # Construir y ejecutar la consulta UPDATE
                query = f"""
                    UPDATE Usuarios SET
                        {', '.join(update_parts)}
                    WHERE IdUser = ?
                """
                
                cursor.execute(query, params)
                connection.commit()
                return {"message": "Usuario actualizado exitosamente"}
                
    except pyodbc.Error as e:
        raise Exception(f"Error al actualizar usuario: {str(e)}")