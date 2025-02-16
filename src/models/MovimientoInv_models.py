from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MovimientoInventario(BaseModel):
    id_MIV: int
    id_producto: int
    cantidad: int
    tipo_movimiento: str
    fecha_movimiento: datetime = Field(default_factory=datetime.now)
    id_user: int
    almacen_id: int
    comentario: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class CreateMovimientoInventario(BaseModel):
    cantidad:int=Field( ge=1, description="Cantidad de producto" )
    tipo_movimiento: str=Field(
        min_length=2, max_length=15, 
        description="Tipo de movimiento"
    )
    id_user:int=Field( gt=0, description="Id del usuario" )
    almacenId:int=Field( gt=0, description="Id del almacen" )

    comentario: Optional[str] = Field(None, max_length=250, description="Comentarios")
    
class UpdateMovimientoInventario(BaseModel): 
    cantidad:Optional[int]=Field(
        None, ge=1, 
        description="Cantidad de producto"
    )
    tipo_movimiento: Optional[str]=Field(
        None, min_length=2, max_length=10, 
        description="Tipo de movimiento"
    )
    id_user:Optional[int]=Field( None, ge=1, description="Id del usuario" )
    almacenId:Optional[int]=Field( None, ge=1, description="Id del almacen" )
    comentario: Optional[str] = Field(None, max_length=250, description="Comentarios")
