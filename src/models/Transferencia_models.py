from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Transferencia(BaseModel):
    id_trasFe: int
    id_producto: int
    cantidad: int
    almacen_origen_id: int
    almacen_destino_id: int
    fecha_transferencia: datetime 
    id_user: int
    comentario: str 

    class Config:
        arbitrary_types_allowed = True

class TransferenciaCreate(BaseModel):
    id_producto: int= Field(gt=0, description="ID del producto")
    cantidad: int = Field(gt=0,description="Cantidad de producto a transferir")
    almacen_origen_id: int = Field(gt=0, description="ID del almacén de origen")
    almacen_destino_id: int = Field(gt=0, description="ID del almacén de destino")
    id_user: int = Field(gt=0, description="ID del usuario que realiza la transferencia")
    comentario: Optional[str] = Field(
        None, max_length=250,
        description="Comentario sobre la transferencia"
    )
    fecha_transferencia: Optional[datetime]



class TransferenciaUpdate(BaseModel):
    # Modelo para actualizar una transferencia existente
    id_producto: Optional[int] = Field(None, description="ID del producto")
    cantidad: Optional[int] = Field(None, description="Cantidad de producto a transferir")
    almacen_origen_id: Optional[int] = Field(None, description="ID del almacén de origen")
    almacen_destino_id: Optional[int] = Field(None, description="ID del almacén de destino")
    id_user: Optional[int] = Field(None, description="ID del usuario que realiza la transferencia")
    comentario: Optional[str] = Field(None, description="Comentario sobre la transferencia")
    estado_transferencia: Optional[str] = Field(None, description="Estado de la transferencia")
    fecha_transferencia: Optional[datetime] = Field(default_factory=datetime.now)

