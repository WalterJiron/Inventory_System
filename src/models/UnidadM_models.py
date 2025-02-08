from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UnidadMedida(BaseModel):
    id: int
    nombre: str
    abreviatura: Optional[str] = None
    estado: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True

class create_update_unidadM(BaseModel):
    NameUnidadM : Optional[str]= Field(
        None,
        min_length=2,
        max_length=25,
        description="Nombre unidad medidad"
    )
    abreviaturaUnidM:Optional[str]=Field(
        None,
        min_length=1,
        max_length=10,
        description="Abreviatura unidad de medida"
    )

