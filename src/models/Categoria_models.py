from pydantic import BaseModel, Field
from typing import Optional


class Categoria(BaseModel):
    id_category: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class create_categoria(BaseModel):
    NameCategoria : str = Field(
        min_length=3, max_length=50,
        description="Nombre de categoria"
    )  
    DescripcionCate: Optional[str]= Field(
        None, min_length=5, max_length=250,
        description="Descripcion de categoria"
    )

class update_categia(BaseModel):
    NameCategoria : Optional[str] = Field(
        None, min_length=3, max_length=25,
        description="Nombre de categoria"
    )  
    DescripcionCate: Optional[str]= Field(
        None, min_length=5, max_length=250,
        description="Descripcion de categoria"
    )

