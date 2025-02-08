from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    id_categoria: int
    proveedor_id: int
    unidad_id: int
    ubicacion_id: int
    sku: Optional[str] = None
    stock: int
    estado: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True

class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del producto")
    precio: float = Field(gt=0, description="Precio del producto")
    id_categoria: int = Field(description="ID de la categoría del producto")
    proveedor_id: int = Field(description="ID del proveedor del producto")
    unidad_id: int = Field(description="ID de la unidad de medida del producto")
    ubicacion_id: int = Field(description="ID de la ubicación del producto")
    sku: Optional[str] = Field(None, max_length=50, description="SKU del producto")
    stock: int = Field(ge=0, description="Stock del producto")

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción del producto")
    precio: Optional[float] = Field(None, gt=0, description="Precio del producto")
    id_categoria: Optional[int] = Field(None, description="ID de la categoría del producto")
    proveedor_id: Optional[int] = Field(None, description="ID del proveedor del producto")
    unidad_id: Optional[int] = Field(None, description="ID de la unidad de medida del producto")
    ubicacion_id: Optional[int] = Field(None, description="ID de la ubicación del producto")
    sku: Optional[str] = Field(None, max_length=50, description="SKU del producto")
    stock: Optional[int] = Field(None, ge=0, description="Stock del producto")
    estado: Optional[bool] = Field(None, description="Estado del producto")

