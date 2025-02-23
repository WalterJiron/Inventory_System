from pydantic import BaseModel, Field 
from typing import Optional
from datetime import datetime 

 
class Rol(BaseModel):
    id_Rol: int
    name_rol: str
    descrip_rl: Optional[str]
    creation_date: datetime 

    class Config: 
        arbitrary_types_allowed = True

class CreateRol(BaseModel):
    NameRol: str = Field(
        min_length=3, max_length=20,
        pattern=r'^[a-zA-Z]+\.?$',
        description="Nombre del rol"
    )
    descrip_rol: Optional[str]= Field(
        None, min_length=3, max_length=250,
        description='Descripcion del rol'
    )

class UpdateRol(BaseModel):
    NameRol: Optional[str] = Field(
        min_length=3, max_length=20,
        pattern=r'^[a-zA-Z]+\.?$',
        descripcion= "Nombre del rol"
    )  
    descrip_rol: Optional[str]= Field(
        None, min_length=3, max_length=250,
         description='Descripcion del rol'
    )
    