from src.models.Categoria_models import Categoria, create_categoria, update_categia
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class CategoryControllers:
    @staticmethod
    def __convert_to_category(category_data: tuple) -> Categoria:
        """Convierte una tupla de datos de la base de datos en un objeto Categoria."""
        return Categoria(
            id_category=category_data[0],
            nombre=category_data[1],
            descripcion=category_data[2]
        )

    @staticmethod
    async def get_category() -> List[Categoria]:
        """Obteniendo todos los datos de las categorias."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """ 
                SELECT IdCategoria, Nombre, Descripcion 
                FROM Categorias
                WHERE Estado = 1;
            """
           
            await loop.run_in_executor(None, cursor.execute, query)
            categorys = await loop.run_in_executor(None, cursor.fetchall)

            return [CategoryControllers.__convert_to_category(category) for category in categorys]
        except Exception as e:
            raise Exception(f"Error al obtener categorias: {str(e)}")

    @staticmethod
    async def get_category_by_id(id_category: int) -> Optional[Categoria]:
        """Obteniendo todos los datos de una categoria."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
           
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """ 
                SELECT IdCategoria, Nombre, Descripcion 
                FROM Categorias
                WHERE IdCategoria = ? AND Estado = 1;
            """
           
            await loop.run_in_executor(None, cursor.execute, query, (id_category,))
            category = await loop.run_in_executor(None, cursor.fetchall)

            if not category:
                return None

            return [CategoryControllers.__convert_to_category(category[0])]
        
        except Exception as e:
            raise Exception(f"Error al obtener categoria por ID: {str(e)}")
        
    @staticmethod
    async def category_create(category: create_categoria) -> dict:
        """Crear una nueva categoria en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
           
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """
                INSERT INTO Categorias(Nombre, Descripcion)
                VALUES(?, ?);
                SELECT SCOPE_IDENTITY() AS IdCategoria;
            """
            
            await loop.run_in_executor(None, cursor.execute, query, (category.NameCategoria, category.DescripcionCate))
            id_category = (await loop.run_in_executor(None, cursor.fetchone))[0]

            await conn.commit()
            return {"message": "Categoria creada exitosamente", "id_Category": id_category}

        except Exception as e:
            raise Exception(f'Error al crear categoria: {str(e)}')
        
    @staticmethod
    def __update_parts(category: update_categia) -> tuple:
        """Construye una lista de partes a actualizar en la base de datos."""
        update_parts = []
        params = []

        if category.NameCategoria is not None:
            update_parts.append('Nombre = ?')
            params.append(category.NameCategoria)
        if category.DescripcionCate is not None:
            update_parts.append('Descripcion = ?')
            params.append(category.DescripcionCate)
        return update_parts, params

    @staticmethod
    async def category_update(id_category: int, category: update_categia) -> dict:
        """Actualiza una categoria existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
           
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query = """
                SELECT Estado 
                FROM Categorias
                WHERE IdCategoria = ? AND Estado = 1;
            """
            
            await loop.run_in_executor(None, cursor.execute, check_query, (id_category,))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                raise Exception("Categoria no encontrada o inactiva")
            
            update_parts, params = CategoryControllers.__update_parts(category)

            if not update_parts:
                raise Exception("No se proporcionaron campos para actualizar.")
            
            params.append(id_category)
            query = f"""
                UPDATE Categorias SET
                    {', '.join(update_parts)}
                WHERE IdCategoria = ?
            """
           
            await loop.run_in_executor(None, cursor.execute, query, params)
            await conn.commit()

            return {"message": "Categoria actualizada exitosamente."}

        except Exception as e:
            raise Exception(f'Error al actualizar categoria: {str(e)}')

    @staticmethod
    async def category_delete(id_category: int) -> dict:
        """Elimina una categoria dentro de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query = """
                SELECT Estado 
                FROM Categorias
                WHERE IdCategoria = ? AND Estado = 1
            """
            
            await loop.run_in_executor(None, cursor.execute, check_query, (id_category,))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                raise Exception("Categoria no encontrada o inactiva")
            
            query = """
                UPDATE Categorias SET
                    Estado = 0
                WHERE IdCategoria = ?
            """
            
            await loop.run_in_executor(None, cursor.execute, query, (id_category,))
            await conn.commit()

            return {"message": "Categoria eliminada exitosamente"}
        
        except Exception as e:
            raise Exception(f'Error al eliminar categoria: {str(e)}')
