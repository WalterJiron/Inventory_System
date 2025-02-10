from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Llamamos de la configuracion de la base de datos
from src.config import ConfigDB

# Clase para manejar la conexion a la base de datos de manera asincrona
class AsyncDBConnection:
    # Almacenamos la instancia unica
    _instance = None

    # Metodo para crear o retornar la instancia existente
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncDBConnection, cls).__new__(cls)
            cls._instance._initialize()  # Inicializa la conexion si no existe
        return cls._instance

    # Inicializa la conexion a la base de datos
    def _initialize(self):
        config = ConfigDB()  # Carga la configuracion de la base de datos

        # Construye la cadena de conexion
        connection_string = (
            f"postgresql+asyncpg://{config.username}:{config.password}@"
            f"{config.server}/{config.database}"
        )

        try:
            # Crea el motor de base de datos asincrono
            self.engine: AsyncEngine = create_async_engine(connection_string, echo=False)

            # Configura el creador de sesiones asincronas
            self.Session = sessionmaker(
                bind=self.engine,
                expire_on_commit=False,
                class_=AsyncSession
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error al inicializar la conexion a la base de datos: {str(e)}")

    # Obtiene una nueva sesion de base de datos asincrona
    async def get_session(self) -> AsyncSession:
        return self.Session()

    # Obtiene el motor de base de datos asincrono
    def get_engine(self) -> AsyncEngine:
        return self.engine

# Funcion asincrona para obtener una conexion a la base de datos
async def get_connection() -> AsyncSession:
    try:
        # Obtiene la instancia de AsyncDBConnection
        db_connection = AsyncDBConnection()
        
        # Obtiene una nueva sesion asincrona
        session = await db_connection.get_session()
        return session
    except Exception as e:
        raise Exception(f"Error al conectar con la base de datos: {str(e)}")
