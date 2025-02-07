import os

# Importacion para cargar variables desde archivo .env
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class ConfigDB:
    def __init__(self):
        # Obtiene las variables de entorno necesarias para la conexion
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_NAME')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

    # Valores por defecto para la configuracion de la base de datos
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_DATABASE = os.getenv('DB_DATABASE', 'GestionInventario')
    DB_USER = os.getenv('DB_USER', 'sa')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
