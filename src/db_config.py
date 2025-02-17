import pymssql
import asyncio
from src.env_config import ConfigDB

# Obtiene los parámetros de conexión
params = ConfigDB().connection_params

async def get_connection():
    try:
        loop = asyncio.get_running_loop()

        # Conexión usando pymssql en un hilo separado
        conn = await loop.run_in_executor(None, lambda: pymssql.connect(
            params['server'],
            params['user'],
            params['password'],
            params['database']
        ))

        return conn
    except Exception as e:
        raise Exception(f"Error al conectar a la base de datos: {str(e)}")
