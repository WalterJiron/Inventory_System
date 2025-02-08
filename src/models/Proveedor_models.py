from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Proveedor(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: Optional[str] = None
    estado: bool = Field(default=True)
    #NOSE SI TE PARECE AGREGAR ESTE 
    """fecha_creacion: datetime = Field(default_factory=datetime.now)"""

    class Config:
        arbitrary_types_allowed = True

class ProveedorCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=50, description="Nombre del proveedor")
    telefono: str = Field(min_length=8, max_length=15, description="Teléfono del proveedor")
    email: str = Field(description="Correo electrónico del proveedor")
    direccion: Optional[str] = Field(None, max_length=250, description="Dirección del proveedor")

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, description="Nombre del proveedor")
    telefono: Optional[str] = Field(None, min_length=8, max_length=15, description="Teléfono del proveedor")
    email: Optional[str] = Field(None, description="Correo electrónico del proveedor")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección del proveedor")
    estado: Optional[bool] = Field(None, description="Estado del proveedor")
