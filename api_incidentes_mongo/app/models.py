from beanie import Document
from pydantic import Field

class Incidente(Document):
    titulo: str = Field(..., max_length=100)
    descripcion: str
    categoria: str
    prioridad: str = "Media"
    estado: str = "Abierto"

    class Settings:
        name = "incidentes"