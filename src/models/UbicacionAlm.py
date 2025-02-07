from pydantic import BaseModel 
from datetime import datetime 


class UbicacionAlmacen(BaseModel):
    id: int
    almacen_id: int
    codigo_ubicacion: str
    descripcion: str | None = None
    capacidad: int | None = None
    estado: bool = True
