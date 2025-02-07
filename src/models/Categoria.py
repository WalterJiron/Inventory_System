from pydantic import BaseModel
from datetime import datetime 

class Categoria(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    estado: bool = True
