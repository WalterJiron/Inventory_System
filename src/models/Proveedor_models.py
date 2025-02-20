from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class Proveedor(BaseModel):
    proveedor_id: int  # Cambio de id_Prov a proveedor_id
    nombre: str
    telefono: str
    email: EmailStr
    direccion: Optional[str] = None
    fecha_creacion: datetime
    estado: bool = True  # Agregado para coincidir con EstadoProv

    class Config:
        arbitrary_types_allowed = True

class ProveedorCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=50)
    telefono: str = Field(regex=r'^\+?[0-9]{8,15}$', min_length=8, max_length=15)
    email: EmailStr
    direccion: Optional[str] = Field(None, max_length=250)
    fecha_creacion: datetime = Field(default_factory=datetime.now)  # Default automático
    estado: bool = True  # Incluido para coherencia con la base de datos

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    telefono: Optional[str] = Field(None, regex=r'^\+?[0-9]{8,15}$', min_length=8, max_length=15)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=250)
    estado: Optional[bool] = None  # Permite actualizar el estado si es necesario

