from pydantic import BaseModel, Field
from typing import Optional


class Categoria(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True

class create_update_categoria(BaseModel):
    NameCategoria : Optional[str] = Field(
        None,
        min_length=3,
        max_length=25,
        description="Nombre de categoria"
    )  
    DescripcionCate: Optional[str]= Field(
        None,
        min_length=5,
        max_length=250,
        description="Descripcion de categoria"
    )

