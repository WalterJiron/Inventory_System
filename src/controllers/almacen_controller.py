from src.models.Almacen_models import Almacen, AlmacenCreate, AlmacenUpdate
from src.DB import get_connection  
from typing import List, Optional

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
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        SELECT AlmacenID, Nombre, Direccion, Capacidad, DateCreate 
                        FROM Almacenes 
                        WHERE Estado = 1
                    """
                    await cursor.execute(query)
                    almacenes = await cursor.fetchall()
                    return [AlmacenesControllers.__convert_to_almacen(almacen) for almacen in almacenes]
                    
        except Exception as e:
            raise Exception(f"Error al obtener almacenes: {str(e)}")
    
    @staticmethod
    async def get_almacen_by_id(almacen_id: int) -> Optional[Almacen]:
        """Obtiene un almacen por su ID si está activo."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        SELECT AlmacenID, Nombre, Direccion, Capacidad, DateCreate 
                        FROM Almacenes 
                        WHERE Estado = 1 AND AlmacenID = ?
                    """
                    await cursor.execute(query, (almacen_id,))
                    almacen = await cursor.fetchone()
                    
                    if almacen is None:
                        return None
                    
                    return AlmacenesControllers.__convert_to_almacen(almacen)
                    
        except Exception as e:
            raise Exception(f"Error al obtener almacen por ID: {str(e)}")
    
    @staticmethod
    async def almacen_create(almacen: AlmacenCreate) -> dict:
        """Crea un nuevo almacen en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        INSERT INTO Almacenes (Nombre, Direccion, Capacidad)
                        VALUES (?, ?, ?);
                        SELECT SCOPE_IDENTITY() AS AlmacenID;
                    """
                    await cursor.execute(query, (almacen.nombre, almacen.direccion, almacen.capacidad))
                    almacen_id = (await cursor.fetchone())[0]
                    await connection.commit()
                    return {"message": "Almacen creado exitosamente", "almacen_id": almacen_id}
                    
        except Exception as e:
            raise Exception(f"Error al crear almacen: {str(e)}")

    @staticmethod 
    async def almacen_update(almacen_id: int, almacen: AlmacenUpdate) -> dict:
        """Actualiza un almacen existente en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    check_query = """
                        SELECT Estado 
                        FROM Almacenes 
                        WHERE AlmacenID = ? AND Estado = 1
                    """
                    await cursor.execute(check_query, (almacen_id,))
                    result = await cursor.fetchone()
                    
                    if not result:
                        raise Exception("Almacen no encontrado o inactivo")
                    
                    update_parts = []
                    params = []
                    
                    if almacen.nombre is not None:
                        update_parts.append("Nombre = ?")
                        params.append(almacen.nombre)
                        
                    if almacen.direccion is not None:
                        update_parts.append("Direccion = ?")
                        params.append(almacen.direccion)
                        
                    if almacen.capacidad is not None:
                        update_parts.append("Capacidad = ?")
                        params.append(almacen.capacidad)
                        
                    if not update_parts:
                        raise Exception("No se proporcionaron campos para actualizar")
                    
                    params.append(almacen_id)
                    
                    query = f"""
                        UPDATE Almacenes SET
                            {', '.join(update_parts)}
                        WHERE AlmacenID = ?
                    """
                    
                    await cursor.execute(query, params)
                    await connection.commit()
                    return {"message": "Almacen actualizado exitosamente"}
                    
        except Exception as e:
            raise Exception(f"Error al actualizar almacén: {str(e)}")

    @staticmethod  
    async def delete_almacen(almacen_id: int) -> dict:
        """Elimina un almacen dentro de la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    check_query = """
                        SELECT Estado 
                        FROM Almacenes 
                        WHERE AlmacenID = ? AND Estado = 1
                    """
                    await cursor.execute(check_query, (almacen_id,))
                    result = await cursor.fetchone()
                    
                    if not result:
                        raise Exception("Almacen no encontrado o inactivo")
                    
                    query = """
                        UPDATE Almacenes SET
                            Estado = 0
                        WHERE AlmacenID = ?
                    """
                    await cursor.execute(query, (almacen_id,))
                    await connection.commit()
                    return {"message": "Almacen eliminado exitosamente"}
                    
        except Exception as e:
            raise Exception(f'Error al eliminar almacen: {str(e)}')