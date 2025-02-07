from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Users(BaseModel):
    id_user: int
    name_user: str
    rol_name: str
    creation_date: datetime

    class Config:
        arbitrary_types_allowed = True

class UserCreate(BaseModel):
    #Modelo para crear un nuevo usuario
    NameUser: str = Field(
        min_length=3, 
        max_length=25,
        description="Nombre del usuario"
    )
    Clave: str = Field(
        min_length=6,
        description="Clave del usuario"
    )
    RolID: int = Field( description="ID del rol del usuario" )

class UserUpdate(BaseModel):
    # Modelo para actualizar un usuario existente
    NameUser: Optional[str] = Field(
        None,
        min_length=3, 
        max_length=25,
        description="Nombre del usuario"
    )
    Clave: Optional[str] = Field(
        None,
        min_length=6,
        description="Contraseña del usuario"
    )
    RolID: Optional[int] = Field( None, description="ID del rol del usuario" )

