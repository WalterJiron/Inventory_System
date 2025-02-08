from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Almacen(BaseModel):
    id: int
    nombre: str
    direccion: Optional[str] = None
    capacidad: Optional[int] = None
    estado: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True

class AlmacenCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=100, description="Nombre del almacén")
    direccion: Optional[str] = Field(None, max_length=255, description="Dirección del almacén")
    capacidad: Optional[int] = Field(None, ge=0, description="Capacidad del almacén")

class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100, description="Nombre del almacén")
    direccion: Optional[str] = Field(None, max_length=255, description="Dirección del almacén")
    capacidad: Optional[int] = Field(None, ge=0, description="Capacidad del almacén")
    estado: Optional[bool] = Field(None, description="Estado del almacén")

