from sqlalchemy import create_engine

# Importacion para manejar sesiones de base de datos
from sqlalchemy.orm import sessionmaker

# Importacion de la configuracion de la base de datos
from src.config import ConfigDB

# Clase para manejar la conexion a la base de datos
class DBConnection:
    # almacenamos la instancia unica 
    _instance = None
    
    # Metodo para crear o retornar la instancia existente
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    # Inicializa la conexion a la base de datos
    def _initialize(self):
        config = ConfigDB()

        # nos conectamso
        connection_string = (
            f"mssql+pyodbc://{config.username}:{config.password}@"
            f"{config.server}/{config.database}?"
            f"driver=ODBC+Driver+17+for+SQL+Server"
        )

        # Crea el motor de base de datos
        self.engine = create_engine(connection_string, echo=False)
        
        # Configura el creador de sesiones
        self.Session = sessionmaker(bind=self.engine)
    
    # Obtiene una nueva sesion de base de datos
    def get_session(self):
        return self.Session()
    
    # Obtiene el motor de base de datos
    def get_engine(self):
        return self.engine