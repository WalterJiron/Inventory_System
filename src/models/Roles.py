from datetime import datetime 
from pydantic import BaseModel

class Rol(BaseModel):
    id: int
    name_rol: str
    creation_date: datetime = datetime.now()
    estado: bool = True

 
