from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Proveedor(BaseModel):
    id_Prov: int
    nombre: str
    telefono: str
    email: str
    direccion: Optional[str] = None
    fecha_creacion: datetime 

    class Config:
        arbitrary_types_allowed = True

class ProveedorCreate(BaseModel):
    nombre: str = Field(
        min_length=3, max_length=50, 
        description="Nombre del proveedor"
    )
    telefono: str = Field(
        regex=r'^[\+\-]?[0-9]{8,15}$', 
        description="Teléfono del proveedor",
        min_length=8, max_length=15
    )
    email: str = Field(
        regex=r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$', 
        description="Correo electrónico del proveedor"
    )
    direccion: Optional[str] = Field(
        None, max_length=250, 
        description="Dirección del proveedor"
    )

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None, min_length=3, max_length=50, 
        description="Nombre del proveedor"
    )
    telefono: Optional[str] = Field(
        None, regex=r'^[\+\-]?[0-9]{8,15}$', 
        min_length=8, max_length=15, 
        description="Teléfono del proveedor"
    )
    email: Optional[str] = Field(
        None, regex=r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$', 
        description="Correo electrónico del proveedor"
    )
    direccion: Optional[str] = Field(
        None, max_length=100, 
        description="Dirección del proveedor"
    )
