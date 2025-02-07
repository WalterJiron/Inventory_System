from pydantic import BaseModel
from datetime import datetime


class Subcategoria(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    id_categoria: int
    estado: bool = True
