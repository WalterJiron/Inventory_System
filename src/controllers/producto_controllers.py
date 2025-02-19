from src.models.Producto_models import Producto, ProductoCreate, ProductoUpdate
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class ProductosControllers:
    @staticmethod
    def __convert_to_producto(producto_data: tuple) -> Producto:
        """Convierte una tupla de datos de la base de datos en un objeto Producto."""
        return Producto(
            id_Produc=producto_data[0],
            nombre=producto_data[1],
            descripcion=producto_data[2],
            precio=producto_data[3],
            id_categoria=producto_data[4],
            proveedor_id=producto_data[5],
            unidad_id=producto_data[6],
            ubicacion_id=producto_data[7],
            sku=producto_data[8],
            stock=producto_data[9],
            fecha_creacion=producto_data[10]
        )

    @staticmethod
    async def get_productos() -> List[Producto]:
        """Obtiene todos los productos activos de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                SELECT * 
                FROM Producto
                WHERE EstadoProduc = 1
            """
            await loop.run_in_executor(None, cursor.execute, query)
            productos = await loop.run_in_executor(None, cursor.fetchall)
            
            return [ProductosControllers.__convert_to_producto(producto) for producto in productos]
        except Exception as e:
            raise Exception(f"Error al obtener productos: {str(e)}")

    @staticmethod
    async def get_producto_by_id(producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID si está activo."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query = """
                SELECT EstadoProduc 
                FROM Producto 
                WHERE IDProducto = ? AND EstadoProduc = 1
            """ 
            await loop.run_in_executor(None, cursor.execute, check_query, (producto_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                raise Exception("Producto no encontrado o inactivo")
            
            query = """
                SELECT * 
                FROM Producto
                WHERE EstadoProduc = 1 AND IDProducto = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (producto_id,))
            producto = await loop.run_in_executor(None, cursor.fetchone)
            
            if producto is None:
                return None
            return ProductosControllers.__convert_to_producto(producto)
        except Exception as e:
            raise Exception(f"Error al obtener el producto por ID: {str(e)}")

    @staticmethod
    async def create_producto(producto: ProductoCreate) -> dict:
        """Crea un nuevo producto en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO Producto (
                    Nombre, Descripcion, Precio, IdCategory, ProveedorID, 
                    UnidadID, UbicacionID, SKU, Stock
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                SELECT SCOPE_IDENTITY() AS IDProducto;
            """
            await loop.run_in_executor(
                None, 
                cursor.execute, 
                query, 
                (
                    producto.nombre,
                    producto.descripcion,
                    producto.precio,
                    producto.id_categoria,
                    producto.proveedor_id,
                    producto.unidad_id,
                    producto.ubicacion_id,
                    producto.sku,
                    producto.stock
                )
            )
            id_producto = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Producto creado exitosamente", "id_Produc": id_producto}
        except Exception as e:
            raise Exception(f"Error al crear el producto: {str(e)}")
        
    @staticmethod
    def __update_parts(producto: ProductoUpdate) -> tuple:
        """Retorna una tupla con los campos a actualizar y sus valores."""
        update_parts = []
        params = []
        
        if producto.nombre is not None:
            update_parts.append("Nombre = ?")
            params.append(producto.nombre)
        if producto.descripcion is not None:
            update_parts.append("Descripcion = ?")
            params.append(producto.descripcion)
        if producto.precio is not None:
            update_parts.append("Precio = ?")
            params.append(producto.precio)
        if producto.id_categoria is not None:
            update_parts.append("IdCategory = ?")
            params.append(producto.id_categoria)
        if producto.proveedor_id is not None:
            update_parts.append("ProveedorID = ?")
            params.append(producto.proveedor_id)
        if producto.unidad_id is not None:
            update_parts.append("UnidadID = ?")
            params.append(producto.unidad_id)
        if producto.ubicacion_id is not None:
            update_parts.append("UbicacionID = ?")
            params.append(producto.ubicacion_id)
        if producto.sku is not None:
            update_parts.append("SKU = ?")
            params.append(producto.sku)
        if producto.stock is not None:
            update_parts.append("Stock = ?")
            params.append(producto.stock)
        
        return update_parts, params

    @staticmethod
    async def update_producto(producto_id: int, producto: ProductoUpdate) -> dict:
        """Actualiza un producto existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT EstadoProduc 
                FROM Producto 
                WHERE IDProducto = ? AND EstadoProduc = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (producto_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Producto no encontrado o inactivo")
            
            update_parts, params = ProductosControllers().__update_parts(producto)
            
            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar")
            
            params.append(producto_id)
            query = f"""
                UPDATE Producto SET
                    {', '.join(update_parts)}
                WHERE IDProducto = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, params)
            await conn.commit()
            
            return {"message": "Producto actualizado exitosamente"}
        except Exception as e:
            raise Exception(f"Error al actualizar el producto: {str(e)}")

    @staticmethod
    async def delete_producto(producto_id: int) -> dict:
        """Elimina un producto de la base de datos (eliminacion logica)."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT EstadoProduc 
                FROM Producto 
                WHERE IDProducto = ? AND EstadoProduc = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (producto_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Producto no encontrado o ya inactivo")
            
            query = """
                UPDATE Producto SET
                    EstadoProduc = 0
                WHERE IDProducto = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (producto_id,))
            await conn.commit()
            
            return {"message": "Producto eliminado exitosamente"}
        except Exception as e:
            raise Exception(f"Error al eliminar el producto: {str(e)}")
