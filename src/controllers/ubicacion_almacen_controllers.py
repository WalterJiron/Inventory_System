from src.models.UbicacionAlm_models import (
    UbicacionAlmacen, UbicacionAlmacenCreate, UbicacionAlmacenUpdate
)
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class UbicacionesAlmacenController:
    @staticmethod
    def __convert_to_ubicacion(ubicacion_data: tuple) -> UbicacionAlmacen:
        """Convierte una tupla de datos de la base de datos en un objeto UbicacionAlmacen."""
        return UbicacionAlmacen(
            id_ubicacio_alamcen=ubicacion_data[0],
            almacen_id=ubicacion_data[1],
            codigo_ubicacion=ubicacion_data[2],
            descripcion=ubicacion_data[3],
            capacidad=ubicacion_data[4],
            fecha_creacion=ubicacion_data[5]
        )

    @staticmethod
    async def get_ubicaciones() -> List[UbicacionAlmacen]:
        """Obtiene todas las ubicaciones activas del almacén."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = "SELECT * FROM UbicacionesAlmacen WHERE Estado = 1"
            await loop.run_in_executor(None, cursor.execute, query)
            ubicaciones = await loop.run_in_executor(None, cursor.fetchall)
            
            return [
                UbicacionesAlmacenController.__convert_to_ubicacion(ubic) 
                for ubic in ubicaciones
            ]
        except Exception as e:
            raise Exception(f"Error al obtener ubicaciones: {str(e)}")

    @staticmethod
    async def get_ubicacion_by_id(ubicacion_id: int) -> Optional[UbicacionAlmacen]:
        """Obtiene una ubicación específica por su ID si está activa."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = "SELECT * FROM UbicacionesAlmacen WHERE UbicacionID = ? AND Estado = 1"
            await loop.run_in_executor(None, cursor.execute, query, (ubicacion_id,))
            ubicacion = await loop.run_in_executor(None, cursor.fetchone)

            if not ubicacion:
                raise Exception("Ubicación no encontrada o inactiva.")
            
            return UbicacionesAlmacenController.__convert_to_ubicacion(ubicacion) 
        except Exception as e:
            raise Exception(f"Error al obtener la ubicación por ID: {str(e)}")

    @staticmethod
    async def create_ubicacion(ubicacion: UbicacionAlmacenCreate) -> dict:
        """Crea una nueva ubicación en el almacén."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO UbicacionesAlmacen (AlmacenID, CodigoUbicacion, Descripcion, Capacidad)
                VALUES (?, ?, ?, ?);
                SELECT SCOPE_IDENTITY() AS UbicacionID;
            """
            await loop.run_in_executor(
                None, cursor.execute, query, (
                    ubicacion.almacen_id,
                    ubicacion.codigo_ubicacion,
                    ubicacion.descripcion,
                    ubicacion.capacidad
                )
            )
            id_ubicacion = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Ubicación creada exitosamente", "id_ubicacion": id_ubicacion}
        except Exception as e:
            raise Exception(f"Error al crear la ubicación: {str(e)}")

    @staticmethod
    def __update_params(ubicacion: UbicacionAlmacenUpdate) -> tuple:
        """Construye las partes de la consulta de actualización."""
        update_parts = []
        params = []
        
        if ubicacion.almacen_id is not None:
            update_parts.append("AlmacenID = ?")
            params.append(ubicacion.almacen_id)
        if ubicacion.codigo_ubicacion is not None:
            update_parts.append("CodigoUbicacion = ?")
            params.append(ubicacion.codigo_ubicacion)
        if ubicacion.descripcion is not None:
            update_parts.append("Descripcion = ?")
            params.append(ubicacion.descripcion)
        if ubicacion.capacidad is not None:
            update_parts.append("Capacidad = ?")
            params.append(ubicacion.capacidad)
        
        return update_parts, params

    @staticmethod
    async def update_ubicacion(ubicacion_id: int, ubicacion: UbicacionAlmacenUpdate) -> dict:
        """Actualiza una ubicación específica."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query ="""
                SELECT UbicacionID FROM UbicacionesAlmacen 
                WHERE UbicacionID = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (ubicacion_id,))
            ubicacion_exists = await loop.run_in_executor(None, cursor.fetchone)

            if not ubicacion_exists:
                raise Exception("Ubicación no encontrada o inactiva.")
            
            update_parts, params = UbicacionesAlmacenController.__update_params(ubicacion)
            
            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar")
            
            params.append(ubicacion_id)
            query = f"""
                UPDATE UbicacionesAlmacen SET
                    {', '.join(update_parts)}
                WHERE UbicacionID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, params)
            await conn.commit()
            
            return {"message": "Ubicación actualizada exitosamente"}
        except Exception as e:
            raise Exception(f"Error al actualizar la ubicación: {str(e)}")

    @staticmethod
    async def delete_ubicacion(ubicacion_id: int) -> dict:
        """Elimina una ubicación del almacén (eliminación lógica)."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query ="""
                SELECT UbicacionID FROM UbicacionesAlmacen 
                WHERE UbicacionID = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (ubicacion_id,))
            ubicacion_exists = await loop.run_in_executor(None, cursor.fetchone)

            if not ubicacion_exists:
                raise Exception("Ubicación no encontrada o ya inactiva.")
            
            query = "UPDATE UbicacionesAlmacen SET Estado = 0 WHERE UbicacionID = ?"
            await loop.run_in_executor(None, cursor.execute, query, (ubicacion_id,))
            delete = await loop.run_in_executor(None, cursor.rowcount)

            if delete == 0:
                raise Exception("Ubicación no encontrada o ya esta inactiva.")
            
            await conn.commit()
            
            return {"message": "Ubicación eliminada exitosamente"}
        except Exception as e:
            raise Exception(f"Error al eliminar la ubicación: {str(e)}")

