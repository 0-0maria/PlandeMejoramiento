from typing import Optional
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class IncidenteBase(BaseModel):
    titulo: str
    descripcion: str
    categoria: str
    prioridad: str
    estado: str

class IncidenteCreate(IncidenteBase):
    pass

class IncidenteUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None

class IncidenteResponse(IncidenteBase):
    id: PydanticObjectId = Field(alias="_id")

    class Config:
        populate_by_name = True