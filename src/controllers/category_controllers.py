from src.models.Categoria_models import Categoria, create_categoria, update_categia
from src.DB import get_connection
from typing import List, Optional

class CategoryControllers:
    @staticmethod
    def __convert_to_category(category_data: tuple) -> Categoria:
        """Convierte una tupla de datos de la base de datos en un objeto Categoria."""
        return Categoria(
            id_category= category_data[0],
            nombre=  category_data[1],
            descripcion= category_data[2]
        )
    
    @staticmethod
    async def get_category() -> List[Categoria]:
        """Obteniendo todos los datos de las categorias."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """ SELECT IdCategoria, Nombre, Descripcion 
                                FROM Categorias
                                WHERE Estado = 1;
                        """
                    await cursor.execute(query)
                    categorys = await cursor.fetchall()

                    return [CategoryControllers.__convert_to_category(category) 
                            for category in categorys]
        except Exception as e:
            raise Exception(f"Error al obtener categorias: {str(e)}")

    @staticmethod
    async def get_category_by_id(id_category: int) -> Optional[Categoria]:
        """Obteniendo todos los datos de una categoria."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    query = """ 
                            SELECT IdCategoria, Nombre, Descripcion 
                            FROM Categorias
                            WHERE IdCategoria = ? AND Estado = 1;
                        """
                    await cursor.execute(query, (id_category))
                    category = await cursor.fetchall()

                    return [ CategoryControllers.__convert_to_category(category) ]
                
        except Exception as e:
            raise Exception(f"Error al obtener categoria: {str(e)}")
        
    @staticmethod
    async def category_create(category: create_categoria) -> dict:
        """Crear una nueva categoria en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with await connection.cursor() as cursor:
                    query = """
                        INSERT INTO Categorias(Nombre, Descripcion)
                        VALUES(?,?);
                        SELECT SCOPE_IDENTITY() AS IdCategoria;
                    """
                    cursor.execute(query,(category.NameCategoria, category.DescripcionCate))

                    id_category = (await cursor.fetchone())[0]
                    await connection.commit()
                    return {"message": "categoria creada exitosamente", "id_Category": id_category}

        except Exception as e:
            raise Exception(f'Error al crear categori: {str(e)}')
        
    @staticmethod
    async def category_update(id_category: int, category: update_categia) -> dict:
        """Actualiza una categoria  existente en la base de datos."""
        try:
            async with await get_connection() as connection:
                async with await connection.cursor as cursor:
                   check_query = """
                        SELECT Estado 
                        FROM Categoria 
                        WHERE IdCategoria = ? AND Estado = 1;
                    """
                   await cursor.execute(check_query, (id_category,))
                   result = await cursor.fetchone()
                   
                   if not result:
                       raise Exception("categoria no encontrado o inactivo")
                   
                   update_parts = []
                   params = []

                   if category.NameCategoria is not None:
                       update_parts.append('Nombre = ?')
                       params.append(category.NameCategoria)

                   if category.DescripcionCate is not None:
                       update_parts.append('Descripcion = ?')
                       params.append(category.DescripcionCate)

                   if not update_parts:
                       raise Exception("No se proporcionaron campos para actualizar.")
                   
                   params.append(id_category)
                   query = f"""
                         UPDATE Categoria SET
                            {', '.join(update_parts)}
                        WHERE IdCategoria = ?
                    """
                   
                   await cursor.execute(query, params)
                   await connection.commit()
                   return {"message": "Categoria actualizada exitosamente."}

        except Exception as e:
            raise Exception(f'Error al actualizar categoria: {str(e)}')

    @staticmethod
    async def category_delete(id_category: int) -> dict:
        """Elimina una categoria dentro de la base de datos."""
        try:
            async with await get_connection() as connection:
                async with connection.cursor() as cursor:
                    check_query = """
                        SELECT Estado 
                        FROM Categoria 
                        WHERE IdCategoria = ? AND Estado = 1
                    """
                    await cursor.execute(check_query, (id_category,))
                    result = await cursor.fetchone()
                    
                    if not result:
                        raise Exception("Categoria no encontrada o inactiva")
                    
                    query = """
                        UPDATE Categoria SET
                            Estado = 0
                        WHERE IdCategoria = ?
                    """
                    await cursor.execute(query, (id_category,))
                    await connection.commit()
                    return {"message": "Categoria eliminada exitosamente"}
                    
        except Exception as e:
            raise Exception(f'Error al eliminar categoria: {str(e)}')     