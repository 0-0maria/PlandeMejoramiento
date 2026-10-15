from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from beanie import PydanticObjectId
from database import init_db
from models import Incidente
from schemas import IncidenteCreate, IncidenteUpdate, IncidenteResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="API Incidentes MongoDB", lifespan=lifespan)

@app.get("/")
def inicio():
    return {"mensaje": "API de Incidentes funcionando con MongoDB"}

@app.get("/incidentes", response_model=list[IncidenteResponse])
async def listar_incidentes():
    return await Incidente.find_all().to_list()

@app.get("/incidentes/{incidente_id}", response_model=IncidenteResponse)
async def obtener_incidente(incidente_id: PydanticObjectId):
    incidente = await Incidente.get(incidente_id)
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente

@app.post("/incidentes", response_model=IncidenteResponse, status_code=201)
async def crear_incidente(datos: IncidenteCreate):
    nuevo = Incidente(**datos.model_dump())
    await nuevo.insert()  


@app.put("/incidentes/{incidente_id}", response_model=IncidenteResponse)
async def actualizar_incidente(incidente_id: PydanticObjectId, datos: IncidenteUpdate):
    incidente = await Incidente.get(incidente_id)
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    cambios = datos.model_dump(exclude_unset=True) 
    for campo, valor in cambios.items():
        setattr(incidente, campo, valor)
    
    await incidente.save()  
    return incidente

@app.delete("/incidentes/{incidente_id}", status_code=204)
async def borrar_incidente(incidente_id: PydanticObjectId):
    incidente = await Incidente.get(incidente_id)
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    await incidente.delete()  