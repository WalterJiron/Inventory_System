from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Llamamos de la configuracion de la base de datos
from src.config import ConfigDB

# Clase para manejar la conexion a la base de datos
class DBConnection:
    # Almacenamos la instancia unica
    _instance = None
    
    # Metodo para crear o retornar la instancia existente
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance._initialize()  # Inicializa la conexion si no existe
        return cls._instance
    
    # Inicializa la conexion a la base de datos
    def _initialize(self):
        config = ConfigDB()  # Carga la configuracion de la base de datos

        # Construye la cadena de conexion
        connection_string = (
            f"mssql+pyodbc://{config.username}:{config.password}@"
            f"{config.server}/{config.database}?"
            f"driver=ODBC+Driver+17+for+SQL+Server"
        )

        try:
            # Crea el motor de base de datos
            self.engine = create_engine(connection_string, echo=False)
            
            # Configura el creador de sesiones
            self.Session = sessionmaker(bind=self.engine)
        except SQLAlchemyError as e:
            raise Exception(f"Error al inicializar la conexion a la base de datos: {str(e)}")
    
    # Obtiene una nueva sesion de base de datos
    def get_session(self):
        return self.Session()
    
    # Obtiene el motor de base de datos
    def get_engine(self):
        return self.engine

# Funcion para obtener una conexion a la base de datos
def get_connection():
    try:
        # Obtiene la instancia de DBConnection
        db_connection = DBConnection()
        
        # Obtiene una nueva sesion
        session = db_connection.get_session()
        return session
    except Exception as e:
        raise Exception(f"Error al conectar con la base de datos: {str(e)}")
