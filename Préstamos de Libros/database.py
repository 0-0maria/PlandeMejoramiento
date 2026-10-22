import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def crear_tabla():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS prestamos(
        id SERIAL PRIMARY KEY,
        libro VARCHAR(150) NOT NULL,
        usuario VARCHAR(100) NOT NULL,
        fecha DATE NOT NULL,
        estado VARCHAR(50) NOT NULL
    )
    """)
    conn.commit()
    cur.close()
    conn.close()