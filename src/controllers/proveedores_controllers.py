from src.models.Proveedor_models import Proveedor, ProveedorCreate, ProveedorUpdate
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class ProveedoresControllers:
    @staticmethod
    def __convert_to_proveedor(proveedor_data: tuple) -> Proveedor:
        """Convierte una tupla de datos de la base de datos en un objeto Proveedor."""
        return Proveedor(
            id_Prov=proveedor_data[0],
            nombre=proveedor_data[1],
            telefono=proveedor_data[2],
            email=proveedor_data[3],
            direccion=proveedor_data[4],
            fecha_creacion=proveedor_data[5],
        )

    @staticmethod
    async def get_proveedores() -> List[Proveedor]:
        """Obtiene todos los proveedores activos de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT ProveedorID, Nombre, Telefono, Email, Direccion, dateCreateProv 
                FROM Proveedores 
                WHERE EstadoProv = 1
            """
            await loop.run_in_executor(None, cursor.execute, query)
            proveedores = await loop.run_in_executor(None, cursor.fetchall)
            
            return [ProveedoresControllers.__convert_to_proveedor(prov) for prov in proveedores]
        
        except Exception as e:
            raise Exception(f"Error al obtener proveedores: {str(e)}")

    @staticmethod
    async def get_proveedor_by_id(id_prov: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID si está activo."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT ProveedorID, Nombre, Telefono, Email, Direccion, dateCreateProv 
                FROM Proveedores 
                WHERE EstadoProv = 1 AND ProveedorID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (id_prov,))
            proveedor = await loop.run_in_executor(None, cursor.fetchone)
            
            if not proveedor:
                raise Exception("Proveedor no encontrado o inactivo")
            
            return ProveedoresControllers.__convert_to_proveedor(proveedor)
        
        except Exception as e:
            raise Exception(f"Error al obtener proveedor por ID: {str(e)}")

    @staticmethod
    async def create_proveedor(prov: ProveedorCreate) -> dict:
        """Crea un nuevo proveedor en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = "SELECT ProveedorID FROM Proveedores WHERE Email = ?"
            await loop.run_in_executor(None, cursor.execute, check_query, (prov.email,))
            existing = await loop.run_in_executor(None, cursor.fetchone)
            if existing:
                raise Exception("El correo electrónico ya está en uso.")
            
            query = """
                INSERT INTO Proveedores (Nombre, Telefono, Email, Direccion)
                VALUES (?, ?, ?, ?);
                SELECT SCOPE_IDENTITY() AS ProveedorID;
            """
            await loop.run_in_executor(None, cursor.execute, query, (prov.nombre, prov.telefono, prov.email, prov.direccion))
            id_prov = (await loop.run_in_executor(None, cursor.fetchone))[0]
            
            await conn.commit()
            return {"message": "Proveedor creado exitosamente", "id_proveedor": id_prov}
        
        except Exception as e:
            raise Exception(f"Error al crear proveedor: {str(e)}")

    @staticmethod
    async def update_proveedor(id_prov: int, prov: ProveedorUpdate) -> dict:
        """Actualiza un proveedor existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = "SELECT EstadoProv FROM Proveedores WHERE ProveedorID = ? AND EstadoProv = 1"
            await loop.run_in_executor(None, cursor.execute, check_query, (id_prov,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            if not result:
                raise Exception("Proveedor no encontrado o inactivo")
            
            update_parts = []
            params = []
            
            if prov.nombre:
                update_parts.append("Nombre = ?")
                params.append(prov.nombre)
            if prov.telefono:
                update_parts.append("Telefono = ?")
                params.append(prov.telefono)
            if prov.email:
                update_parts.append("Email = ?")
                params.append(prov.email)
            if prov.direccion:
                update_parts.append("Direccion = ?")
                params.append(prov.direccion)
            
            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar")
            
            params.append(id_prov)
            query = f"""
                UPDATE Proveedores SET
                    {', '.join(update_parts)}
                WHERE ProveedorID = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, params)
            await conn.commit()
            return {"message": "Proveedor actualizado exitosamente"}
        
        except Exception as e:
            raise Exception(f"Error al actualizar proveedor: {str(e)}")

