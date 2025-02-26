from src.db_config import get_connection
import asyncio

class LoginController:
    @staticmethod
    async def check_login(username: str, password: str) -> bool:
        """Valida las credenciales del usuario."""
        try:
            conn = await get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            
            loop = asyncio.get_event_loop()
            cursor = await loop.run_in_executor(None, conn.cursor)
            
            # Verificar si el usuario existe
            query_user = """
                SELECT IdUser, EstadoUser 
                FROM Usuarios
                WHERE NameUser = ?;
            """
            await loop.run_in_executor(None, cursor.execute, query_user, (username,))
            user = await loop.run_in_executor(None, cursor.fetchone)
            
            if user is None:
                return {"error": "Usuario no encontrado"}
            
            user_id, estado_user = user
            if not estado_user:
                raise Exception({"error": "El usuario se encuentra deshabilitado"})
            
            # Verificar la contraseña
            query_password = """
                SELECT Clave 
                FROM Usuarios
                WHERE IdUser = ?;
            """
            await loop.run_in_executor(None, cursor.execute, query_password, (user_id,))
            stored_password = await loop.run_in_executor(None, cursor.fetchone)
            
            if stored_password is None or stored_password[0] != password:
                raise Exception({"error": "Contraseña incorrecta"})
            
            return True
        except Exception as e:
            raise Exception({"error": f"Error al validar credenciales: {str(e)}"})