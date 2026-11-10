from fastapi import FastAPI, HTTPException
import os
import psycopg2
from pydantic import BaseModel

app = FastAPI(title="API DataMart - Ticket Promedio 125053083")

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "datamart_db"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "secret123")
    )

@app.get("/resultados")
def obtener_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, tienda, ticket_promedio FROM resultados_ticket_promedio ORDER BY tienda;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "tienda": r[1], "ticket_promedio": float(r[2])} for r in rows]

@app.get("/resultados/{tienda}")
def obtener_por_tienda(tienda: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, tienda, ticket_promedio FROM resultados_ticket_promedio WHERE tienda ILIKE %s;", (tienda,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return [{"id": r[0], "tienda": r[1], "ticket_promedio": float(r[2])} for r in rows]

class Registro(BaseModel):
    tienda: str
    ticket_promedio: float

@app.post("/resultados")
def crear_registro(item: Registro):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO resultados_ticket_promedio (tienda, ticket_promedio) VALUES (%s, %s) RETURNING id;", (item.tienda, item.ticket_promedio))
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": nuevo_id, "mensaje": "Registro insertado"}

@app.delete("/resultados/{id}")
def eliminar_registro(id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM resultados_ticket_promedio WHERE id = %s RETURNING id;", (id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="ID no encontrado")
    return {"mensaje": f"Registro {id} eliminado"}
