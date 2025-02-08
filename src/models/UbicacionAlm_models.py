from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UbicacionAlmacen(BaseModel):
    id: int
    almacen_id: int
    codigo_ubicacion: str
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None
    estado: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True

class UbicacionAlmacenCreate(BaseModel):
    almacen_id: int = Field(description="ID del almacén")
    codigo_ubicacion: str = Field(min_length=1, max_length=50, description="Código de la ubicación dentro del almacén")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción de la ubicación")
    capacidad: Optional[int] = Field(None, ge=0, description="Capacidad de la ubicación")

class UbicacionAlmacenUpdate(BaseModel):
    almacen_id: Optional[int] = Field(None, description="ID del almacén")
    codigo_ubicacion: Optional[str] = Field(None, min_length=1, max_length=50, description="Código de la ubicación dentro del almacén")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción de la ubicación")
    capacidad: Optional[int] = Field(None, ge=0, description="Capacidad de la ubicación")
    estado: Optional[bool] = Field(None, description="Estado de la ubicación")

