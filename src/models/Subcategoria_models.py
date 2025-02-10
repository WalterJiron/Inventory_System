from pydantic import BaseModel, Field
from typing import Optional


class Subcategoria(BaseModel):
    id_SubCate: int
    nombre: str
    descripcion: Optional[str] 
    id_categoria: int

    class Config:
        arbitrary_types_allowed = True

class CreateSubCategoria(BaseModel):
    NameSubCategoria:str = Field(
        min_length=10, max_length=100,
        description="Nombre de Subcategoria"
    )
    DescriptionSubCate : Optional[str] = Field(
        None, min_length=10, max_length=250,
        description="descripcion de la Subcategoria"

    )
    IdCategoria: int = Field( None, description="Id de categoria" )


class UpdateSubCategoria(BaseModel):
    NameSubCategoria:Optional[str] = Field(
        None, min_length=10, max_length=100,
        description="Nombre de Subcategoria"
    )
    DescriptionSubCate : Optional[str] = Field(
        None, min_length=10, max_length=250,
        description="descripcion de la Subcategoria"

    )
    IdCategoria:Optional[int] = Field( None, description="Id de categoria" )
