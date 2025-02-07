from pydantic import BaseModel
from datetime import datetime 

 
class Usuario(BaseModel):
    id: int
    name_user: str
    clave: str
    rol_id: int
    creation_date: datetime = datetime.now()
    estado: bool = True

