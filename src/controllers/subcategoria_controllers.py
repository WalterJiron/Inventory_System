from src.models.Subcategoria_models import Subcategoria, CreateSubCategoria, UpdateSubCategoria
from src.db_config import get_connection
from typing import List, Optional
import asyncio

class SubcategoriaControllers:
    @staticmethod
    def __convert_to_subcategoria(subcategoria_data: tuple) -> Subcategoria:
        """Convierte una tupla de datos de la base de datos en un objeto Subcategoria."""
        return Subcategoria(
            id_SubCate=subcategoria_data[0],
            nombre=subcategoria_data[1],
            descripcion=subcategoria_data[2],
            id_categoria=subcategoria_data[3]
        )

    @staticmethod
    async def create_subcategoria(subcategoria: CreateSubCategoria) -> dict:
        """Crea una nueva subcategoría en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            query = """
                INSERT INTO Subcategoria (
                    nombre, descripcion, idCategoria
                ) VALUES (?, ?, ?);
                SELECT SCOPE_IDENTITY() AS id_subcategoria;
            """
            await loop.run_in_executor(
                None, 
                cursor.execute, 
                query, 
                (
                    subcategoria.NameSubCategoria,
                    subcategoria.DescriptionSubCate,
                    subcategoria.IdCategoria
                )
            )
            id_subcategoria = (await loop.run_in_executor(None, cursor.fetchone))[0]
            await conn.commit()
            
            return {"message": "Subcategoría creada exitosamente", "id_subcategoria": id_subcategoria}
        except Exception as e:
            raise Exception(f"Error al crear la subcategoría: {str(e)}")

    @staticmethod
    async def get_subcategorias() -> List[Subcategoria]:
        """Obtiene todas las subcategorías activas de la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se puede conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            query = """
                SELECT * 
                FROM Subcategoria 
                WHERE Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, query)
            subcategorias = await loop.run_in_executor(None, cursor.fetchall)

            return [SubcategoriaControllers.__convert_to_subcategoria(subcategoria) for subcategoria in subcategorias]
        except Exception as e:
            raise Exception(f"Error al obtener las subcategorías: {str(e)}")

    @staticmethod
    async def get_subcategoria_by_id(subcategoria_id: int) -> Optional[Subcategoria]:
        """Obtiene una subcategoría por su ID si está activa."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se puede conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)

            check_query = """
                SELECT * 
                FROM Subcategoria 
                WHERE Estado = 1 AND id_subcategoria = ?
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (subcategoria_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)

            if not result:
                raise Exception("Subcategoría no encontrada o inactiva")
            
            return SubcategoriaControllers.__convert_to_subcategoria(result)
        except Exception as e:
            raise Exception(f"Error al obtener la subcategoría por ID: {str(e)}")

    @staticmethod
    def __update_parts(subcategoria: UpdateSubCategoria) -> tuple:
        """Retorna una tupla con los campos a actualizar y sus valores."""
        update_parts = []
        params = []
        
        if subcategoria.NameSubCategoria is not None:
            update_parts.append("nombre = ?")
            params.append(subcategoria.NameSubCategoria)
        if subcategoria.DescriptionSubCate is not None:
            update_parts.append("descripcion = ?")
            params.append(subcategoria.DescriptionSubCate)
        if subcategoria.IdCategoria is not None:
            update_parts.append("idCategoria = ?")
            params.append(subcategoria.IdCategoria)
        
        return update_parts, params

    @staticmethod
    async def update_subcategoria(subcategoria_id: int, subcategoria: UpdateSubCategoria) -> dict:
        """Actualiza una subcategoría existente en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT Estado 
                FROM Subcategoria 
                WHERE id_subcategoria = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (subcategoria_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Subcategoría no encontrada o inactiva")
            
            update_parts, params = SubcategoriaControllers.__update_parts(subcategoria)
            if not update_parts:
                raise Exception("No hay campos para actualizar")
            
            query = f"""
                UPDATE Subcategoria 
                SET {', '.join(update_parts)} 
                WHERE id_subcategoria = ?
            """
            params.append(subcategoria_id)
            
            await loop.run_in_executor(None, cursor.execute, query, tuple(params))
            await conn.commit()
            
            return {"message": "Subcategoría actualizada exitosamente"}
        except Exception as e:
            raise Exception(f"Error al actualizar la subcategoría: {str(e)}")

    @staticmethod
    async def deactivate_subcategoria(subcategoria_id: int) -> dict:
        """Desactiva una subcategoría en la base de datos."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            check_query = """
                SELECT Estado 
                FROM Subcategoria 
                WHERE id_subcategoria = ? AND Estado = 1
            """
            await loop.run_in_executor(None, cursor.execute, check_query, (subcategoria_id,))
            result = await loop.run_in_executor(None, cursor.fetchone)
            
            if not result:
                raise Exception("Subcategoría no encontrada o ya está inactiva")
            
            query = """
                UPDATE Subcategoria 
                SET Estado = 0 
                WHERE id_subcategoria = ?
            """
            await loop.run_in_executor(None, cursor.execute, query, (subcategoria_id,))
            await conn.commit()
            
            return {"message": "Subcategoría desactivada exitosamente"}
        except Exception as e:
            raise Exception(f"Error al desactivar la subcategoría: {str(e)}")
