from src.models.Almacen_models import Almacen, AlmacenCreate, AlmacenUpdate
from src.db_config import get_connection  
from typing import List, Optional
import asyncio

class AlmacenesControllers:
    @staticmethod
    def __convert_to_almacen(almacen_data: tuple) -> Almacen:
        """Convierte una tupla de datos de la base de datos en un objeto Almacen."""
        return Almacen(
            id_Amacen=almacen_data[0],
            nombre=almacen_data[1],
            direccion=almacen_data[2],
            capacidad=almacen_data[3],
            fecha_creacion=almacen_data[4]
        )

    @staticmethod
    async def get_almacenes() -> List[Almacen]:
        """Obtiene todos los almacenes activos de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_running_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """
                SELECT AlmacenID, Nombre, Direccion, Capacidad, DateCreate 
                FROM Almacenes 
                WHERE Estado = 1;
            """
            await loop.run_in_executor(None, cursor.execute, query)
            almacenes = await loop.run_in_executor(None, cursor.fetchall)
            
            # Cerrar cursor y conexión
            cursor.close()
            conn.close()
            
            return [AlmacenesControllers.__convert_to_almacen(almacen) 
                    for almacen in almacenes]
                    
        except Exception as e:
            raise Exception(f"Error al obtener almacenes: {str(e)}")

    @staticmethod
    async def get_almacen_by_id(almacen_id: int) -> Optional[Almacen]:
        """Obtiene un almacén por su ID si está activo."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_running_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT AlmacenID, Nombre, Direccion, Capacidad, DateCreate 
                FROM Almacenes 
                WHERE Estado = 1 AND AlmacenID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (almacen_id,))
            almacen = await loop.run_in_executor(None, cursor.fetchone)
            
            cursor.close()
            conn.close()
            
            if almacen is None:
                return None
            
            return AlmacenesControllers.__convert_to_almacen(almacen)
                    
        except Exception as e:
            raise Exception(f"Error al obtener almacén por ID: {str(e)}")

    @staticmethod
    async def almacen_create(almacen: AlmacenCreate) -> dict:
        """Crea un nuevo almacén en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_running_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO Almacenes (Nombre, Direccion, Capacidad)
                VALUES (?, ?, ?);
                SELECT SCOPE_IDENTITY() AS AlmacenID;
            """
            await loop.run_in_executor(None, cursor.execute, query, (almacen.nombre, almacen.direccion, almacen.capacidad))
            almacen_id = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await loop.run_in_executor(None, conn.commit)
            
            cursor.close()
            conn.close()
            
            return {"message": "Almacén creado exitosamente", "almacen_id": almacen_id}
                    
        except Exception as e:
            raise Exception(f"Error al crear almacén: {str(e)}")

    @staticmethod
    def __update_parts(almacen: AlmacenUpdate) -> tuple:
        """Construye las partes de la consulta de actualizacion."""
        update_parts = []
        params = []
        
        if almacen.nombre:
            update_parts.append("Nombre = ?")
            params.append(almacen.nombre)
        if almacen.direccion:
            update_parts.append("Direccion = ?")
            params.append(almacen.direccion)
        if almacen.capacidad:
            update_parts.append("Capacidad = ?")
            params.append(almacen.capacidad)
        
        return update_parts, params

    @staticmethod 
    async def almacen_update(almacen_id: int, almacen: AlmacenUpdate) -> dict:
        """Actualiza un almacén existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_running_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT Estado 
                FROM Almacenes 
                WHERE AlmacenID = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (almacen_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Almacén no encontrado o inactivo")
            
            update_parts, params = AlmacenesControllers.__update_parts(almacen)
                        
            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar")
            
            params.append(almacen_id)
            
            query = f"""
                UPDATE Almacenes SET
                    {', '.join(update_parts)}
                WHERE AlmacenID = ?
            """
                    
            await loop.run_in_executor(None, cursor.execute, query, params)
            await loop.run_in_executor(None, conn.commit)
            
            cursor.close()
            conn.close()
            
            return {"message": "Almacén actualizado exitosamente"}
                    
        except Exception as e:
            raise Exception(f"Error al actualizar almacén: {str(e)}")

    @staticmethod  
    async def delete_almacen(almacen_id: int) -> dict:
        """Elimina un almacen dentro de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_running_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT Estado 
                FROM Almacenes 
                WHERE AlmacenID = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (almacen_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Almacén no encontrado o inactivo")
            
            query = """
                UPDATE Almacenes SET
                    Estado = 0
                WHERE AlmacenID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (almacen_id,))
            await loop.run_in_executor(None, conn.commit)
            
            cursor.close()
            conn.close()
            
            return {"message": "Almacén eliminado exitosamente"}
                    
        except Exception as e:
            raise Exception(f"Error al eliminar almacén: {str(e)}")
