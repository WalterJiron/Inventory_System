from src.models.producto_models import Producto, ProductoCreate, ProductoUpdate
from src.BD import get_connection
from typing import List, Optional

class ProductoControllers:
    @staticmethod
    def __convert_to_producto(producto_data: tuple) -> Producto:
        """Convierte una tupla de datos de la base de datos en una clase Producto."""
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
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        SELECT * 
                        FROM Producto
                        WHERE EstadoProduc = 1;
                    """
                    await cursor.execute(query)
                    productos = await cursor.fetchall()
                    return [ProductoControllers.__convert_to_producto(producto) 
                            for producto in productos]
        except Exception as e:
            raise Exception(f"Error al obtener productos: {str(e)}")

    @staticmethod
    async def get_producto_by_id(producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID si está activo."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        SELECT * 
                        FROM Producto
                        WHERE EstadoProduc = 1 AND IDProducto = ?;
                    """
                    await cursor.execute(query, (producto_id,))
                    producto = await cursor.fetchone()

                    if producto is None:
                        return None
                    return ProductoControllers.__convert_to_producto(producto)
        except Exception as e:
            raise Exception(f"Error al obtener el producto por ID: {str(e)}")

    @staticmethod
    async def create_producto(producto: ProductoCreate) -> dict:
        """Crea un nuevo producto en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """
                        INSERT INTO Producto (
                            Nombre, Descripcion, Precio, IdCategory, ProveedorID, 
                            UnidadID, UbicacionID, SKU, Stock
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """
                    await cursor.execute(query, (
                        producto.nombre,
                        producto.descripcion,
                        producto.precio,
                        producto.id_categoria,
                        producto.proveedor_id,
                        producto.unidad_id,
                        producto.ubicacion_id,
                        producto.sku,
                        producto.stock
                    ))
                    await connection.commit()

                    # Obtener el ID del producto recién creado
                    producto_id = cursor.lastrowid

                    return {"message": "Producto creado exitosamente", "id_Produc": producto_id}
        except Exception as e:
            raise Exception(f"Error al crear el producto: {str(e)}")

    @staticmethod
    async def update_producto(producto_id: int, producto: ProductoUpdate) -> dict:
        """Actualiza un producto existente en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    # Verificar si el producto existe y está activo
                    check_query = """
                        SELECT EstadoProduc 
                        FROM Producto 
                        WHERE IDProducto = ? AND EstadoProduc = 1
                    """
                    await cursor.execute(check_query, (producto_id,))
                    result = await cursor.fetchone()

                    if not result:
                        raise Exception("Producto no encontrado o inactivo")

                    # Construir la consulta dinámica
                    update_parts = []
                    params = []

                    if producto.nombre is not None:
                        update_parts.append("nombre = ?")
                        params.append(producto.nombre)

                    if producto.descripcion is not None:
                        update_parts.append("descripcion = ?")
                        params.append(producto.descripcion)

                    if producto.precio is not None:
                        update_parts.append("precio = ?")
                        params.append(producto.precio)

                    if producto.id_categoria is not None:
                        update_parts.append("id_categoria = ?")
                        params.append(producto.id_categoria)

                    if producto.proveedor_id is not None:
                        update_parts.append("proveedor_id = ?")
                        params.append(producto.proveedor_id)

                    if producto.unidad_id is not None:
                        update_parts.append("unidad_id = ?")
                        params.append(producto.unidad_id)

                    if producto.ubicacion_id is not None:
                        update_parts.append("ubicacion_id = ?")
                        params.append(producto.ubicacion_id)

                    if producto.sku is not None:
                        update_parts.append("sku = ?")
                        params.append(producto.sku)

                    if producto.stock is not None:
                        update_parts.append("stock = ?")
                        params.append(producto.stock)

                    if not update_parts:
                        raise Exception("No se proporcionaron campos para actualizar")

                    # Agregar el ID del producto al final de los parámetros
                    params.append(producto_id)

                    # Construir la consulta final
                    query = f"""
                        UPDATE Producto SET
                            {', '.join(update_parts)}
                        WHERE IDProducto = ?
                    """

                    await cursor.execute(query, params)
                    await connection.commit()

                    return {"message": "Producto actualizado exitosamente"}

        except Exception as e:
            raise Exception(f"Error al actualizar el producto: {str(e)}")

    @staticmethod
    async def delete_producto(producto_id: int) -> dict:
        """Elimina un producto de la base de datos (eliminación lógica)."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    # Verificar si el producto existe y está activo
                    check_query = """
                        SELECT EstadoProduc 
                        FROM Producto 
                        WHERE IDProducto = ? AND EstadoProduc = 1
                    """
                    await cursor.execute(check_query, (producto_id,))
                    result = await cursor.fetchone()

                    if not result:
                        raise Exception("Producto no encontrado o ya está inactivo")

                    # Realizar la eliminación lógica (establecer Estado = 0)
                    query = """
                        UPDATE Producto SET
                            EstadoProduc = 0
                        WHERE IDProducto = ?
                    """
                    await cursor.execute(query, (producto_id,))
                    await connection.commit()

                    return {"message": "Producto eliminado exitosamente"}

        except Exception as e:
            raise Exception(f"Error al eliminar el producto: {str(e)}")
