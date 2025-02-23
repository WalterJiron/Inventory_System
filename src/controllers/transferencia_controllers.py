from src.models.Transferencia_models import (
    Transferencia, TransferenciaCreate, TransferenciaUpdate
)
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class TransferenciasControllers:
    @staticmethod
    def __convert_to_transferencia(data: tuple) -> Transferencia:
        """Convierte una tupla de datos de la base de datos en un objeto Transferencia."""
        return Transferencia(
            id_trasFe=data[0],
            id_producto=data[1],
            cantidad=data[2],
            almacen_origen_id=data[3],
            almacen_destino_id=data[4],
            fecha_transferencia=data[5],
            id_user=data[6],
            comentario=data[7]
        )

    @staticmethod
    async def get_transferencias() -> List[Transferencia]:
        """Obtiene todas las transferencias de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT * FROM Transferencias
                WHERE EstadoTransferencia = 1;
            """
            await loop.run_in_executor(None, cursor.execute, query)
            transferencias = await loop.run_in_executor(None, cursor.fetchall)

            if not transferencias:
                raise Exception("No se encontraron transferencias.")
            
            return [
                TransferenciasControllers.__convert_to_transferencia(tr) 
                for tr in transferencias
            ]
        
        except Exception as e:
            raise Exception(f"Error al obtener transferencias: {str(e)}")

    @staticmethod
    async def get_transferencia_by_id(id_trasFe: int) -> Optional[Transferencia]:
        """Obtiene una transferencia por su ID."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT * FROM Transferencias 
                WHERE TransferenciaID = ? AND EstadoTransferencia = 1;
            """
            await loop.run_in_executor(None, cursor.execute, query, (id_trasFe))
            transferencia = await loop.run_in_executor(None, cursor.fetchone)
            
            if not transferencia:
                raise Exception("Transferencia no encontrada.")
            
            return TransferenciasControllers.__convert_to_transferencia(transferencia)
        
        except Exception as e:
            raise Exception(f"Error al obtener transferencia por ID: {str(e)}")

    @staticmethod
    async def create_transferencia(transferencia: TransferenciaCreate) -> dict:
        """Crea una nueva transferencia en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO Transferencias 
                (IDProducto, Cantidad, AlmacenOrigenID, AlmacenDestinoID, IdUser, Comentario)
                VALUES (?, ?, ?, ?, ?, ?);
                SELECT SCOPE_IDENTITY() AS TransferenciaID;
            """
            
            await loop.run_in_executor(
                None, cursor.execute, query, 
                (
                    transferencia.id_producto,
                    transferencia.cantidad,
                    transferencia.almacen_origen_id,
                    transferencia.almacen_destino_id,
                    transferencia.id_user,
                    transferencia.comentario
                )
            )
            id_transferencia = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Transferencia creada exitosamente", "id_transferencia": id_transferencia}
        
        except Exception as e:
            raise Exception(f"Error al crear transferencia: {str(e)}")

    def __update_params(transferencia: TransferenciaUpdate) -> tuple:
        """Construye los campos a actualizar en la base de datos."""
        update_parts = []
        params = []
        
        if transferencia.id_producto:
            update_parts.append("IDProducto = ?")
            params.append(transferencia.id_producto)
        if transferencia.cantidad:
            update_parts.append("Cantidad = ?")
            params.append(transferencia.cantidad)
        if transferencia.almacen_origen_id:
            update_parts.append("AlmacenOrigenID = ?")
            params.append(transferencia.almacen_origen_id)
        if transferencia.almacen_destino_id:
            update_parts.append("AlmacenDestinoID = ?")
            params.append(transferencia.almacen_destino_id)
        if transferencia.id_user:
            update_parts.append("IdUser = ?")
            params.append(transferencia.id_user)
        if transferencia.comentario:
            update_parts.append("Comentario = ?")
            params.append(transferencia.comentario)
        if transferencia.estado_transferencia:
            update_parts.append("EstadoTransferencia = ?")
            params.append(transferencia.estado_transferencia)
        
        return update_parts, params 

    @staticmethod
    async def update_transferencia(id_trasFe: int, transferencia: TransferenciaUpdate) -> dict:
        """Actualiza una transferencia existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query = """
                SELECT EstadoTransferencia 
                FROM Transferencias 
                WHERE TransferenciaID = ? AND EstadoTransferencia = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (id_trasFe))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                raise Exception("Transferencia no encontrada o inactiva")
            
            update_parts, params = TransferenciasControllers.__update_params(transferencia)
            
            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar")
            
            params.append(id_trasFe)
            query = f"""
                UPDATE Transferencias
                SET {', '.join(update_parts)}
                WHERE TransferenciaID = ?
            """
            
            await loop.run_in_executor(None, cursor.execute, query, tuple(params))
            await conn.commit()
            
            return {"message": "Transferencia actualizada exitosamente"}
        
        except Exception as e:
            raise Exception(f"Error al actualizar transferencia: {str(e)}")
    
    @staticmethod
    async def delete_transferencia(id_trasFe: int)->dict:
        """ELimina la transferencia dentro de la base de datos """
        try:
            conn= await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la Base de datos")

            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                    SELECT EstadoTransferencia 
                    FROM Transferencias 
                    WHERE TransferenciaID = ? AND EstadoTransferencia = 1
            """ 
            await loop.run_in_executor( None, cursor.execute, check_query, (id_trasFe,))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                    raise Exception("Usuario no encontrado")
            query = """
                    UPDATE transferencias SET
                            EstadoTransferencia = 0
                    WHERE TransferenciaID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (id_trasFe,))
            await conn.commit()
            return{"message" : "Transferencia eliminado exitosamente"}
        except Exception as e:
            raise Exception(f"Error al eliminar la transferencia: {str(e)}")




