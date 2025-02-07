from pydantic import BaseModel
from datetime import datetime   

 
class Proveedor(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str | None = None
    estado: bool = True
