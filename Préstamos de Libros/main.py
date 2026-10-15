from fastapi import FastAPI, HTTPException
from database import crear_tabla, get_connection
from models import Prestamo

app = FastAPI()

crear_tabla()

@app.get("/")
def inicio():
    return {"mensaje": "API de Préstamos de Libros funcionando"}

@app.get("/prestamos")
def listar_prestamos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, libro, usuario, fecha, estado FROM prestamos ORDER BY id")
    prestamos = cur.fetchall()
    cur.close()
    conn.close()
    return prestamos

@app.get("/prestamos/{id}")
def buscar_prestamo(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, libro, usuario, fecha, estado FROM prestamos WHERE id = %s", (id,))
    prestamo = cur.fetchone()
    cur.close()
    conn.close()
    if prestamo:
        return prestamo
    raise HTTPException(status_code=404, detail="Préstamo no encontrado")

@app.post("/prestamos")
def crear_prestamo(prestamo: Prestamo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO prestamos (libro, usuario, fecha, estado) VALUES (%s, %s, %s, %s) RETURNING id",
        (prestamo.libro, prestamo.usuario, prestamo.fecha, prestamo.estado)
    )
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Préstamo creado", "id": nuevo_id}

@app.put("/prestamos/{id}")
def actualizar_prestamo(id: int, prestamo: Prestamo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE prestamos SET libro = %s, usuario = %s, fecha = %s, estado = %s WHERE id = %s",
        (prestamo.libro, prestamo.usuario, prestamo.fecha, prestamo.estado, id)
    )
    filas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return {"mensaje": "Préstamo actualizado"}

@app.delete("/prestamos/{id}")
def eliminar_prestamo(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM prestamos WHERE id = %s", (id,))
    filas = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return {"mensaje": "Préstamo eliminado"}