from src.models.MovimientoInv_models import  MovimientoInventario, CreateMovimientoInventario, UpdateMovimientoInventario
from src.BD import  get_connection
from typing import List, Optional

class MovimientoInventarioControllers:
    @staticmethod
    def __convert_to_movimiento(movimiento_data: tuple) -> MovimientoInventario:
        """Convierte una tupla de datos de la base de datos en una clase MovimientoInventario"""
        return MovimientoInventario(    
            id_MIV = movimiento_data[0],
            id_producto = movimiento_data[1],
            cantidad = movimiento_data[2],
            tipo_movimiento =  movimiento_data[3],
            fecha_movimiento =  movimiento_data[4],
            id_user=  movimiento_data[5],
            almacen_id=  movimiento_data[6],
            comentario=  movimiento_data[7]
        )
    
    @staticmethod
    async def get_movimiento_inventario() -> List[MovimientoInventario]:
        """Obtiene todos los MovimientoInventario activos de la base de datos"""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query  = """ 
                            SELECT * 
                            FROM MovimientoInventario
                            WHERE EstadoMovimiento = 1;
                    """

                    await cursor.execute(query)
                    movimientos = await.cursor.fetchall()
                    return [MovimientoInventarioControllers.__convert_to_movimiento(movimientos)
                        for movimiento in movimientos]
        except Exception as e:
            raise Exception(f"Error al obtener MovimientoInventario: {str(e)}")

    @staticmethod
    async def get_movimiento_inventario_by_id(movimiento_id: int) -> Optional[MovimientoInventario]:
        """Obtiene los MovimientoInventario por su id si esta activo"""
        try:
             async with await get_connection() as connection:
                 async with connection.cursor() as cursor:
                     query = """ 
                            SELECT * 
                            FROM MovimientoInventario
                            WHERE EstadoMovimiento = 1 AND id_MIV = ?
                     """ 
                    await cursor.execute(query, (movimiento_id,))
                    movimiento = await cursor.fetchone()

                    if movimiento is None:
                        return None
                    return MovimientoInventarioControllers.__convert_to_movimiento(movimiento)
         except Exception as e:
            raise Exception(f"Error al obtener el movimiento por ID: {str(e)}")

    @staticmethod
    async def movimiento_create(movimiento: CreateMovimientoInventario) -> dict:
        """Crea un nuevo MovimientoInventario en la BD"""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        INSERT INTO MovimientoInventario (
                            id_producto, cantidad, tipo_movimiento, fecha_movimiento, id_user, almacen_id, comentario
                        ) VALUES (?, ?, ?, ?, ?);
                    """
                    await cursor.execute(query, (
                        movimiento.cantidad,
                        movimiento.tipo_movimiento,
                        movimiento.id_user,
                        movimiento.almacen_id,
                        movimiento.comentario
                    ))
                    await connection.commit()

                    # Obtener el ID del movimiento recién creado
                    movimiento_id = cursor.lastrowid

                    return {"message": "Movimiento creado exitosamente", "id_MIV": movimiento_id}
        except Exception as e:
            raise Exception(f"Error al crear el movimiento: {str(e)}")

    @staticmethod
    async def update(movimiento_id: int, movimiento: UpdateMovimientoInventario) -> dict:
        """Actualiza un MovimientoInventario existente en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    # Verificar si el movimiento existe y está activo
                    check_query = """
                        SELECT EstadoMovimiento 
                        FROM MovimientoInventario 
                        WHERE id_MIV = ? AND EstadoMovimiento = 1
                    """
                    await cursor.execute(check_query, (movimiento_id,))
                    result = await cursor.fetchone()

                    if not result:
                        raise Exception("Movimiento no encontrado o inactivo")

                    # Construir la consulta dinámica
                    update_parts = []
                    params = []

                    if movimiento.cantidad is not None:
                        update_parts.append("cantidad = ?")
                        params.append(movimiento.cantidad)

                    if movimiento.tipo_movimiento is not None:
                        update_parts.append("tipo_movimiento = ?")
                        params.append(movimiento.tipo_movimiento)

                    if movimiento.id_user is not None:
                        update_parts.append("id_user = ?")
                        params.append(movimiento.id_user)

                    if movimiento.almacen_id is not None:
                        update_parts.append("almacen_id = ?")
                        params.append(movimiento.almacen_id)

                    if movimiento.comentario is not None:
                        update_parts.append("comentario = ?")
                        params.append(movimiento.comentario)

                    if not update_parts:
                        raise Exception("No se proporcionaron campos para actualizar")

                    # Agregar el ID del movimiento al final de los parámetros
                    params.append(movimiento_id)

                    # Construir la consulta final
                    query = f"""
                        UPDATE MovimientoInventario SET
                            {', '.join(update_parts)}
                        WHERE id_MIV = ?
                    """

                    await cursor.execute(query, params)
                    await connection.commit()

                    return {"message": "Movimiento actualizado exitosamente"}

        except Exception as e:
            raise Exception(f"Error al actualizar el movimiento: {str(e)}")


    @staticmethod
    async def delete(movimiento_id: int) -> dict:
        """Elimina un movimiento de inventario dentro de la base de datos (eliminación lógica)."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    # Verificar si el movimiento existe y está activo
                    check_query = """
                        SELECT EstadoMovimiento 
                        FROM MovimientoInventario 
                        WHERE id_MIV = ? AND EstadoMovimiento = 1
                    """
                    await cursor.execute(check_query, (movimiento_id,))
                    result = await cursor.fetchone()

                    if not result:
                        raise Exception("Movimiento no encontrado o ya está inactivo")

                    # Realizar la eliminación lógica (establecer EstadoMovimiento = 0)
                    query = """
                        UPDATE MovimientoInventario SET
                            EstadoMovimiento = 0
                        WHERE id_MIV = ?
                    """
                    await cursor.execute(query, (movimiento_id,))
                    await connection.commit()

                    return {"message": "Movimiento eliminado exitosamente"}

        except Exception as e:
            raise Exception(f"Error al eliminar el movimiento: {str(e)}")
