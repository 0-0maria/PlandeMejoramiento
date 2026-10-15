from pydantic import BaseModel
from datetime import date

class Prestamo(BaseModel):
    libro: str
    usuario: str
    fecha: date
    estado: str