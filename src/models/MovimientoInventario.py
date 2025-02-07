from pydantic import BaseModel
from datetime import datetime 



class MovimientoInventario(BaseModel):
    id: int
    id_producto: int
    cantidad: int
    tipo_movimiento: str
    fecha_movimiento: datetime = datetime.now()
    id_user: int
    almacen_id: int
    comentario: str | None = None
    estado: bool = True
