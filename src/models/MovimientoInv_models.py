from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MovimientoInventario(BaseModel):
    id: int
    id_producto: int
    cantidad: int
    tipo_movimiento: str
    fecha_movimiento: datetime = Field(default_factory=datetime.now)
    id_user: int
    almacen_id: int
    comentario: Optional[str] = None
    estado: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True

class CreateMovimientoInventario(BaseModel):
    id_producto:int=Field(None, description="id del producto")
    cantidad:int=Field(None, min_length=1, description="Cantidad de producto")
    tipo_movimiento: str=Field(None, min_length=2, max_length=10, description="Tipo de movimiento")
    id_user:int=Field(None, description="Id del usuario")
    almacenId:int=Field(None, description="Id del almacen")
    comentario: Optional[str] = Field(None, max_length=250, description="Comentarios")
    
class UpdateMovimientoInventario(BaseModel):
    id_producto:Optional[int]=Field(None, description="id del producto")
    cantidad:Optional[int]=Field(None, min_length=1, description="Cantidad de producto")
    tipo_movimiento: Optional[str]=Field(None, min_length=2, max_length=10, description="Tipo de movimiento")
    id_user:Optional[int]=Field(None, description="Id del usuario")
    almacenId:Optional[int]=Field(None, description="Id del almacen")
    comentario: Optional[str] = Field(None, max_length=250, description="Comentarios")
    estado:Optional[int]=Field(None, description="Estado")