from pydantic import BaseModel
from datetime import datetime   


class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    precio: float
    id_categoria: int
    proveedor_id: int
    unidad_id: int
    ubicacion_id: int
    sku: str | None = None
    stock: int
    estado: bool = True





