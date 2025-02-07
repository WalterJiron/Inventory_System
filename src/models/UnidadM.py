from pydantic import BaseModel
from datetime import datetime   


class UnidadMedida(BaseModel):
    id: int
    nombre: str
    abreviatura: str | None = None
    estado: bool = True
