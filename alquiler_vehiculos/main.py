from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import Base, engine, get_db, historial_collection
import models, schemas, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Alquiler de Vehículos - SENA", version="1.0.0")

@app.get("/")
def inicio():
    return {"mensaje": "API de Alquiler de Vehículos activa"}


@app.post("/registro", response_model=dict, status_code=201)
def registrar_usuario(usuario: schemas.UsuarioRegistro, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.username == usuario.username).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    nuevo_usuario = models.Usuario(
        username=usuario.username,
        password_hash=auth.hashear_password(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    return {"mensaje": "Usuario creado exitosamente"}

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == form_data.username).first()
    if not usuario or not auth.verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = auth.crear_token({"sub": usuario.username, "id": usuario.id})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/customers", response_model=list[schemas.CustomerResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()

@app.post("/customers", response_model=schemas.CustomerResponse, status_code=201)
def crear_cliente(cliente: schemas.CustomerCreate, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    nuevo = models.Customer(**cliente.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/customers/{cliente_id}", response_model=schemas.CustomerResponse)
def actualizar_cliente(cliente_id: int, datos: schemas.CustomerCreate, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    cliente = db.query(models.Customer).filter(models.Customer.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in datos.model_dump().items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente

@app.delete("/customers/{cliente_id}", status_code=204)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    cliente = db.query(models.Customer).filter(models.Customer.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()


@app.get("/vehicles", response_model=list[schemas.VehicleResponse])
def listar_vehiculos(db: Session = Depends(get_db)):
    return db.query(models.Vehicle).all()

@app.post("/vehicles", response_model=schemas.VehicleResponse, status_code=201)
def crear_vehiculo(vehiculo: schemas.VehicleCreate, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    nuevo = models.Vehicle(**vehiculo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/vehicles/{vehiculo_id}", response_model=schemas.VehicleResponse)
def actualizar_vehiculo(vehiculo_id: int, datos: schemas.VehicleCreate, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    vehiculo = db.query(models.Vehicle).filter(models.Vehicle.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    for key, value in datos.model_dump().items():
        setattr(vehiculo, key, value)
    db.commit()
    db.refresh(vehiculo)
    return vehiculo

@app.delete("/vehicles/{vehiculo_id}", status_code=204)
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    vehiculo = db.query(models.Vehicle).filter(models.Vehicle.id == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    db.delete(vehiculo)
    db.commit()


@app.get("/rentals", response_model=list[schemas.RentalResponse])
def listar_alquileres(db: Session = Depends(get_db)):
    return db.query(models.Rental).all()

@app.get("/rentals/{rental_id}", response_model=schemas.RentalResponse)
def obtener_alquiler(rental_id: int, db: Session = Depends(get_db)):
    alquiler = db.query(models.Rental).filter(models.Rental.id == rental_id).first()
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return alquiler

@app.post("/rentals", response_model=schemas.RentalResponse, status_code=201)
def crear_alquiler(alquiler: schemas.RentalCreate, db: Session = Depends(get_db), usuario=Depends(auth.obtener_usuario_actual)):
    cliente = db.query(models.Customer).filter(models.Customer.id == alquiler.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Regla de Negocio: No se puede registrar alquiler, el cliente no existe")

    vehiculo = db.query(models.Vehicle).filter(models.Vehicle.id == alquiler.vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Regla de Negocio: No se puede registrar alquiler, el vehículo no existe")

    dias = (alquiler.fecha_final - alquiler.fecha_inicial).days
    if dias <= 0:
        dias = 1
    total = dias * vehiculo.precio_por_dia

    nuevo_alquiler = models.Rental(
        cliente_id=alquiler.cliente_id,
        vehiculo_id=alquiler.vehiculo_id,
        fecha_inicial=alquiler.fecha_inicial,
        fecha_final=alquiler.fecha_final,
        valor_total=total
    )
    db.add(nuevo_alquiler)
    db.commit()
    db.refresh(nuevo_alquiler)

    documento_mongo = {
        "rental_id_pg": nuevo_alquiler.id,
        "cliente": cliente.nombre,
        "correo": cliente.correo,
        "vehiculo": f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.placa})",
        "fecha_inicial": str(alquiler.fecha_inicial),
        "fecha_final": str(alquiler.fecha_final),
        "valor_total": total
    }
    historial_collection.insert_one(documento_mongo)

    return nuevo_alquiler

@app.get("/alquileres-mongo")
def consultar_historial_mongo():
    registros = list(historial_collection.find({}, {"_id": 0}))
    return {"historial_mongodb": registros}