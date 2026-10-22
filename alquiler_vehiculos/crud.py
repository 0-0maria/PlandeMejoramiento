from sqlalchemy.orm import Session
import models
import schemas

def obtener_servicios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Servicio).offset(skip).limit(limit).all()

def obtener_servicio(db: Session, servicio_id: int):
    return db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()

def crear_servicio(db: Session, servicio: schemas.ServicioCreate):
    db_servicio = models.Servicio(
        nombre=servicio.nombre,
        precio=servicio.precio,
        estado=servicio.estado
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio

def actualizar_servicio(db: Session, servicio_id: int, servicio: schemas.ServicioCreate):
    db_servicio = obtener_servicio(db, servicio_id)
    if not db_servicio:
        return None
    db_servicio.nombre = servicio.nombre
    db_servicio.precio = servicio.precio
    db_servicio.estado = servicio.estado
    db.commit()
    db.refresh(db_servicio)
    return db_servicio

def eliminar_servicio(db: Session, servicio_id: int):
    db_servicio = obtener_servicio(db, servicio_id)
    if not db_servicio:
        return None
    db.delete(db_servicio)
    db.commit()
    return db_servicio