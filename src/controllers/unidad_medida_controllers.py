from src.models.UnidadM_models import UnidadMedida, create_unidadM, update_unidadM
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class UnidadMedidaControllers:
    @staticmethod
    def __convert_to_unidad_medida(unidad_medida_data: tuple) -> UnidadMedida:
        """Convierte una tupla de datos de la base de datos en un objeto UnidadMedida."""
        return UnidadMedida(
            id_UM=unidad_medida_data[0],
            nombre=unidad_medida_data[1],
            abreviatura=unidad_medida_data[2]
        )

    @staticmethod
    async def create_unidad_medida(unidad_medida: create_unidadM) -> dict:
        """Crea una nueva unidad de medida en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO UnidadesMedida ( Nombre, Abreviatura ) 
                VALUES (?, ?);
                SELECT SCOPE_IDENTITY() AS UnidadID;
            """
            await loop.run_in_executor(
                None, cursor.execute, query, (
                    unidad_medida.NameUnidadM, unidad_medida.abreviaturaUnidM 
                )
            )
            id_unidad_medida = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Unidad de medida creada exitosamente", "id_unidad_medida": id_unidad_medida}
        except Exception as e:
            raise Exception(f"Error al crear la unidad de medida: {str(e)}")

    @staticmethod
    async def get_unidades_medida() -> List[UnidadMedida]:
        """Obtiene todas las unidades de medida activas de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se puede conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """
                SELECT * 
                FROM UnidadesMedida 
                WHERE Estado = 1;
            """
            await loop.run_in_executor(None, cursor.execute, query)
            unidades_medida = await loop.run_in_executor(None, cursor.fetchall)

            return [
                UnidadMedidaControllers.__convert_to_unidad_medida(unidad) 
                for unidad in unidades_medida
            ]
        except Exception as e:
            raise Exception(f"Error al obtener las unidades de medida: {str(e)}")

    @staticmethod
    async def get_unidad_medida_by_id(unidad_id: int) -> Optional[UnidadMedida]:
        """Obtiene una unidad de medida por su ID si está activa."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se puede conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """
                SELECT * 
                FROM UnidadesMedida 
                WHERE Estado = 1 AND UnidadID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (unidad_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                raise Exception("Unidad de medida no encontrada o inactiva")
            
            return UnidadMedidaControllers.__convert_to_unidad_medida(result)
        except Exception as e:
            raise Exception(f"Error al obtener la unidad de medida por ID: {str(e)}")

    @staticmethod
    def __update_parts(unidad_medida: update_unidadM) -> tuple:
        """Retorna una tupla con los campos a actualizar y sus valores."""
        update_parts = []
        params = []
        
        if unidad_medida.NameUnidadM is not None:
            update_parts.append("Nombre = ?")
            params.append(unidad_medida.NameUnidadM)
        if unidad_medida.abreviaturaUnidM is not None:
            update_parts.append("Abreviatura = ?")
            params.append(unidad_medida.abreviaturaUnidM)
        
        return update_parts, params

    @staticmethod
    async def update_unidad_medida(unidad_id: int, unidad_medida: update_unidadM) -> dict:
        """Actualiza una unidad de medida existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT Estado 
                FROM UnidadesMedida 
                WHERE UnidadID = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (unidad_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Unidad de medida no encontrada o inactiva")
            
            update_parts, params = UnidadMedidaControllers.__update_parts(unidad_medida)
            
            if not update_parts:
                raise Exception("No hay campos para actualizar")
            
            query = f"""
                UPDATE UnidadesMedida 
                SET {', '.join(update_parts)} 
                WHERE UnidadID = ?
            """
            params.append(unidad_id)
            
            await loop.run_in_executor(None, cursor.execute, query, tuple(params))
            await conn.commit()
            
            return {"message": "Unidad de medida actualizada exitosamente"}
        except Exception as e:
            raise Exception(f"Error al actualizar la unidad de medida: {str(e)}")

    @staticmethod
    async def deactivate_unidad_medida(unidad_id: int) -> dict:
        """Desactiva una unidad de medida en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT Estado 
                FROM UnidadesMedida 
                WHERE UnidadID = ? AND Estado = 1;
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (unidad_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Unidad de medida no encontrada o ya está inactiva")
            
            query = """
                UPDATE UnidadesMedida 
                SET Estado = 0 
                WHERE UnidadID = ?;
            """
            await loop.run_in_executor(None, cursor.execute, query, (unidad_id,))
            await conn.commit()
            
            return {"message": "Unidad de medida desactivada exitosamente"}
        except Exception as e:
            raise Exception(f"Error al desactivar la unidad de medida: {str(e)}")
