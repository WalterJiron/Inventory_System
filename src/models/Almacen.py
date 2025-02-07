from pydantic import BaseModel
from datetime  import datetime  

class Almacen(BaseModel):
    id: int
    nombre: str
    direccion: str | None = None
    capacidad: int | None = None
    estado: bool = True
