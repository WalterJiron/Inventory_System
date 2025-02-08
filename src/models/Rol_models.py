from pydantic import BaseModel, Field 
from typing import Optional
from datetime import datetime 

 
class Rol(BaseModel):
    id: int
    name_rol: str
    creation_date: datetime = Field(default_factory=datetime.now)
    estado: bool = Field(default=True)

    class Config: 
        arbitrary_types_allowed = True

class create_update_rol(BaseModel):
    NameRol: Optional[str] = Field(
        None,
        min_length=3,
        max_length=20,
        descripcion= "Nombre del rol"
    )  
    
