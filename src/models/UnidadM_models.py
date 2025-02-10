from pydantic import BaseModel, Field
from typing import Optional


class UnidadMedida(BaseModel):
    id_UM: int
    nombre: str
    abreviatura: str

    class Config:
        arbitrary_types_allowed = True

class create_unidadM(BaseModel):
    NameUnidadM : str= Field(
        min_length=2, max_length=25,
        description="Nombre unidad medidad"
    )
    abreviaturaUnidM:str=Field(
        min_length=3, max_length=10,
        description="Abreviatura unidad de medida"
    )

class update_unidadM(BaseModel):
    NameUnidadM : Optional[str]= Field(
        None, min_length=2, max_length=25,
        description="Nombre unidad medidad"
    )
    abreviaturaUnidM:Optional[str]=Field(
        None, min_length=3, max_length=10,
        description="Abreviatura unidad de medida"
    )

