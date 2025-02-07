from pydantic import BaseModel
from datetime import datetime 


class Transferencia(BaseModel):
    id: int
    id_producto: int
    cantidad: int
    almacen_origen_id: int
    almacen_destino_id: int
    fecha_transferencia: datetime = datetime.now()
    id_user: int
    comentario: str | None = None
    estado_transferencia: str
