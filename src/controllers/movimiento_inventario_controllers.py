from src.models.MovimientoInv_models import MovimientoInventario, CreateMovimientoInventario, UpdateMovimientoInventario
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class MovimientoInventarioControllers:
    @staticmethod
    def __convert_to_movimiento(movimiento_data: tuple) -> MovimientoInventario:
        """Convierte una tupla de datos de la base de datos en un objeto MovimientoInventario."""
        return MovimientoInventario(
            id_MIV=movimiento_data[0],
            id_producto=movimiento_data[1],
            cantidad=movimiento_data[2],
            tipo_movimiento=movimiento_data[3],
            fecha_movimiento=movimiento_data[4],
            id_user=movimiento_data[5],
            almacen_id=movimiento_data[6],
            comentario=movimiento_data[7]
        )

    @staticmethod
    async def get_movimiento_inventario() -> List[MovimientoInventario]:
        """Obtiene todos los movimientos de inventario activos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT id_MIV, id_producto, cantidad, tipo_movimiento, fecha_movimiento, id_user, almacen_id, comentario
                FROM MovimientoInventario
                WHERE EstadoMovimiento = 1
            """
            await loop.run_in_executor(None, cursor.execute, query)
            movimientos = await loop.run_in_executor(None, cursor.fetchall)
            
            return [MovimientoInventarioControllers.__convert_to_movimiento(movimiento) for movimiento in movimientos]
        
        except Exception as e:
            raise Exception(f"Error al obtener movimientos de inventario: {str(e)}")

    @staticmethod
    async def get_movimiento_inventario_by_id(movimiento_id: int) -> Optional[MovimientoInventario]:
        """Obtiene un movimiento de inventario por su ID si está activo."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query = """
                SELECT EstadoMovimiento
                FROM MovimientoInventario
                WHERE id_MIV = ? AND EstadoMovimiento = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (movimiento_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Movimiento no encontrado o inactivo")
            
            query = """
                SELECT id_MIV, id_producto, cantidad, tipo_movimiento, fecha_movimiento, id_user, almacen_id, comentario
                FROM MovimientoInventario
                WHERE EstadoMovimiento = 1 AND id_MIV = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (movimiento_id,))
            movimiento = await loop.run_in_executor(None, cursor.fetchone)
            
            if movimiento is None:
                return None
            return MovimientoInventarioControllers.__convert_to_movimiento(movimiento)
        
        except Exception as e:
            raise Exception(f"Error al obtener el movimiento por ID: {str(e)}")

    @staticmethod
    async def create_movimiento_inventario(movimiento: CreateMovimientoInventario) -> dict:
        """Crea un nuevo movimiento de inventario."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO MovimientoInventario (id_producto, cantidad, tipo_movimiento, fecha_movimiento, id_user, almacen_id, comentario)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                SELECT SCOPE_IDENTITY() AS id_MIV;
            """
            await loop.run_in_executor(None, cursor.execute, query, (
                movimiento.id_producto, movimiento.cantidad, movimiento.tipo_movimiento,
                movimiento.fecha_movimiento, movimiento.id_user, movimiento.almacen_id, movimiento.comentario
            ))
            
            id_miv = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Movimiento creado exitosamente", "id_MIV": id_miv}
        
        except Exception as e:
            raise Exception(f"Error al crear movimiento de inventario: {str(e)}")

    @staticmethod
    def __update_movimiento_parts(movimiento: UpdateMovimientoInventario) -> tuple:
        """Construye una tupla con los campos a actualizar y sus valores."""
        update_parts = []
        params = []
        
        if movimiento.cantidad is not None:
            update_parts.append("cantidad = ?")
            params.append(movimiento.cantidad)
        
        if movimiento.tipo_movimiento is not None:
            update_parts.append("tipo_movimiento = ?")
            params.append(movimiento.tipo_movimiento)
        
        if movimiento.fecha_movimiento is not None:
            update_parts.append("fecha_movimiento = ?")
            params.append(movimiento.fecha_movimiento)
        
        if movimiento.id_user is not None:
            update_parts.append("id_user = ?")
            params.append(movimiento.id_user)
        
        if movimiento.almacen_id is not None:
            update_parts.append("almacen_id = ?")
            params.append(movimiento.almacen_id)
        
        if movimiento.comentario is not None:
            update_parts.append("comentario = ?")
            params.append(movimiento.comentario)
        
        return update_parts, params

    @staticmethod
    async def update_movimiento_inventario(movimiento_id: int, movimiento: UpdateMovimientoInventario) -> dict:
        """Actualiza un movimiento de inventario existente."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT EstadoMovimiento
                FROM MovimientoInventario
                WHERE id_MIV = ? AND EstadoMovimiento = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (movimiento_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Movimiento no encontrado o inactivo")
            
            update_parts, params = MovimientoInventarioControllers.__update_movimiento_parts(movimiento)
            
            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar")
            
            params.append(movimiento_id)
            
            query = f"""
                UPDATE MovimientoInventario SET
                    {', '.join(update_parts)}
                WHERE id_MIV = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, tuple(params))
            await conn.commit()
            
            return {"message": "Movimiento actualizado exitosamente"}
        
        except Exception as e:
            raise Exception(f"Error al actualizar el movimiento: {str(e)}")

    @staticmethod
    async def delete_movimiento_inventario(movimiento_id: int) -> dict:
        """Elimina un movimiento de inventario (eliminación lógica)."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT EstadoMovimiento
                FROM MovimientoInventario
                WHERE id_MIV = ? AND EstadoMovimiento = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (movimiento_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Movimiento no encontrado o inactivo")
            
            query = """
                UPDATE MovimientoInventario
                SET EstadoMovimiento = 0
                WHERE id_MIV = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (movimiento_id,))
            await conn.commit()
            
            return {"message": "Movimiento eliminado exitosamente"}
        
        except Exception as e:
            raise Exception(f"Error al eliminar el movimiento: {str(e)}")
