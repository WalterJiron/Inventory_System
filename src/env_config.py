import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class ConfigDB:
    def __init__(self):
        # Obtiene las variables de entorno necesarias para la conexion
        self.server = self._get_env_variable('DB_SERVER')
        self.database = self._get_env_variable('DB_DATABASE')
        self.username = self._get_env_variable('DB_USER')
        self.password = self._get_env_variable('DB_PASSWORD')

    def _get_env_variable(self, var_name):
        """Obtiene una variable de entorno y lanza una excepcion si no esta definida"""
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"{var_name} no esta definida en el archivo .env")
        return value

    @property
    def connection_params(self):
        """Retorna los parametros de conexion como un diccionario para pymssql"""
        return {
            'server': self.server,
            'user': self.username,
            'password': self.password,
            'database': self.database
        }
