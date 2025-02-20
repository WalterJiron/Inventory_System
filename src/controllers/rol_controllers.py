from src.models.Rol_models import Rol, CreateRol, UpdateRol
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class RolControllers:
    @staticmethod
    def __convert_to_rol(rol_data:tuple) -> Rol:
        """Convierte una tupla de datos de la base de datos en un objeto Rol"""
        return Rol(
            id_Rol = rol_data[0],
            name_rol = rol_data[1],
            descrip_rl=rol_data[2],
            creation_date=rol_data[3]
        )
    
    @staticmethod
    async def get_rol() -> List[Rol]:
        """Obtiene todos los roles activos de la base de datos """
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se puede conectar a la base de datos")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """
                SELECT * 
                FROM Roles 
                WHERE EstadoRol = 1
            """
            await loop.run_in_executor(None,cursor.execute, query)
            rols = await loop.run_in_executor(None, cursor.fetchall)

            return [RolControllers.__convert_to_rol(rol) for rol in rols]
        except Exception as e:
            raise Exception(f"Error al obtener productos: {str(e)}")

    @staticmethod
    async def get_rol_by_id(rol_id: int) -> Optional[Rol]:
        """Obtiene un rol por su ID si esta activo.""" 
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se puede conectar a la base de datos")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
                    
            query ="""
                    SELECT * 
                    FROM Producto
                    WHERE EstadoRol = 1 AND RolID = ?
                    """ 
            await loop.run_in_executor(None, cursor.execute, query, (rol_id))
            rol = await loop.run_in_executor(None, cursor.fetchone)
            
            if not rol:
                raise Exception("Rol no encontrado o inactivo")
            
            return RolControllers.__convert_to_producto(rol)
        except Exception as e:
            raise Exception(f"Error al obtener el rol por id: {str(e)}")
       
    @staticmethod
    async def create_rol(rol: CreateRol) -> dict:
        """Crea un nuevo rol en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO Roles ( NameRol, DescripRol ) 
                VALUES (?, ?);
                SELECT SCOPE_IDENTITY() AS RolID;
            """
            await loop.run_in_executor(
                None, cursor.execute, query, ( rol.NameRol, rol.descrip_rol )
            )
            id_rol = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Rol creado exitosamente", "id_Rol": id_rol}
        except Exception as e:
            raise Exception(f"Error al crear el rol: {str(e)}")

    @staticmethod
    def __update_parts(rol: UpdateRol) -> tuple:
        """Retorna una tupla con los campos a actualizar y sus valores."""
        update_parts = []
        params = []
        
        if rol.NameRol is not None:
            update_parts.append("NameRol = ?")
            params.append(rol.NameRol)
        if rol.descrip_rol is not None:
            update_parts.append("DescripRol = ?")
            params.append(rol.descrip_rol)
        
        return update_parts, params

    @staticmethod
    async def update_rol(rol_id: int, rol: UpdateRol) -> dict:
        """Actualiza un rol existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT EstadoRol 
                FROM Roles 
                WHERE RolID = ? AND EstadoRol = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (rol_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Rol no encontrado o inactivo")
            
            update_parts, params = RolControllers.__update_parts(rol)
            if not update_parts:
                raise Exception("No hay campos para actualizar")
            
            query = f"""
                UPDATE Roles 
                SET {', '.join(update_parts)} 
                WHERE RolID = ?
            """
            params.append(rol_id)
            
            await loop.run_in_executor(None, cursor.execute, query, tuple(params))
            await conn.commit()
            
            return {"message": "Rol actualizado exitosamente"}
        except Exception as e:
            raise Exception(f"Error al actualizar el rol: {str(e)}")

    @staticmethod
    async def deactivate_rol(rol_id: int) -> dict:
        """Desactiva un rol en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT EstadoRol 
                FROM Roles 
                WHERE RolID = ? AND EstadoRol = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (rol_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Rol no encontrado o ya está inactivo")
            
            query = """
                UPDATE Roles 
                SET EstadoRol = 0 
                WHERE RolID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (rol_id,))
            await conn.commit()
            
            return {"message": "Rol desactivado exitosamente"}
        except Exception as e:
            raise Exception(f"Error al desactivar el rol: {str(e)}")
