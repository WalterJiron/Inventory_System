from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UbicacionAlmacen(BaseModel):
    id_ubicacio_alamcen: int
    almacen_id: int
    codigo_ubicacion: str
    descripcion: Optional[str] 
    capacidad: Optional[int] 
    fecha_creacion: datetime

    class Config:
        arbitrary_types_allowed = True

class UbicacionAlmacenCreate(BaseModel):
    almacen_id: int = Field(gt=0, description="ID del almacén")
    codigo_ubicacion: str = Field(
        min_length=3, max_length=50, 
        description="Código de la ubicación dentro del almacén")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción de la ubicación")
    capacidad: Optional[int] = Field(0, ge=0, description="Capacidad de la ubicación")

class UbicacionAlmacenUpdate(BaseModel):
    almacen_id: Optional[int] = Field(None, description="ID del almacén")
    codigo_ubicacion: Optional[str] = Field(
        None, min_length=3, max_length=50, 
        description="Código de la ubicación dentro del almacén"
    )
    descripcion: Optional[str] = Field(
        None, min_length=3, max_length=255, 
        description="Descripción de la ubicación"
    )
    capacidad: Optional[int] = Field(0, ge=0, description="Capacidad de la ubicación")

