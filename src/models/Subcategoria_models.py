from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Subcategoria(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    id_categoria: int
    estado: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True

class CreateSubCategoria(BaseModel):
    NameSubCategoria:str = Field(
        None,
        min_length=10,
        max_length=100,
        description="Nombre de Subcategoria"
    )
    DescriptionSubCate : str = Field(
        None,
        min_length=10,
        max_length=250,
        description="descripcion de la Subcategoria"

    )
    IdCategoria: int = Field(
        None,
        description="Id de categoria"
    )


class UpdateSubCategoria(BaseModel):
    NameSubCategoria:Optional[str] = Field(
        None,
        min_length=10,
        max_length=100,
        description="Nombre de Subcategoria"
    )
    DescriptionSubCate : Optional[str] = Field(
        None,
        min_length=10,
        max_length=250,
        description="descripcion de la Subcategoria"

    )
    IdCategoria:Optional[int] = Field(
        None,
        description="Id de categoria"
    )
