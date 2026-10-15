from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UsuarioRegistro(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CustomerBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    class Config:
        from_attributes = True

class VehicleBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    precio_por_dia: float
    disponible: bool = True

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    class Config:
        from_attributes = True

class RentalCreate(BaseModel):
    cliente_id: int
    vehiculo_id: int
    fecha_inicial: date
    fecha_final: date

class RentalResponse(BaseModel):
    id: int
    cliente_id: int
    vehiculo_id: int
    fecha_inicial: date
    fecha_final: date
    valor_total: float

    class Config:
        from_attributes = True