from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Almacen(BaseModel):
    id_Amacen: int
    nombre: str
    direccion: str
    capacidad: int
    fecha_creacion: datetime 

    class Config:
        arbitrary_types_allowed = True

class AlmacenCreate(BaseModel):
    nombre: str = Field(
        min_length=3, max_length=100, 
        description="Nombre del almacén"
    )
    direccion: str = Field(
        min_length=5, max_length=255, 
        description="Dirección del almacén" 
    )
    capacidad: Optional[int] = Field(
        None, gt=0, 
        description="Capacidad del almacén"
    )

class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None, 
        min_length=3,
        max_length=100, 
        description="Nombre del almacén"
    )

    direccion: Optional[str] = Field(
        None, 
        max_length=255, 
        description="Dirección del almacén"
    )

    capacidad: Optional[int] = Field(
        None, 
        gt=0, 
        description="Capacidad del almacén"
    )