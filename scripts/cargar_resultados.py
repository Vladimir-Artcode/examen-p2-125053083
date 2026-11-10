import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    database=os.getenv("DB_NAME", "datamart_db"),
    user=os.getenv("DB_USER", "admin"),
    password=os.getenv("DB_PASSWORD", "secret123")
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS resultados_ticket_promedio (
        id SERIAL PRIMARY KEY,
        tienda VARCHAR(50),
        ticket_promedio NUMERIC(14, 2)
    );
""")
cur.execute("TRUNCATE TABLE resultados_ticket_promedio RESTART IDENTITY;")
conn.commit()

ruta_salida = "/data/mapreduce/output/part-00000"
with open(ruta_salida, "r", encoding="utf-8") as f:
    for line in f:
        partes = line.strip().split("\t")
        if len(partes) == 2:
            tienda, promedio = partes
            cur.execute(
                "INSERT INTO resultados_ticket_promedio (tienda, ticket_promedio) VALUES (%s, %s);",
                (tienda, float(promedio))
            )

conn.commit()
cur.close()
conn.close()
print("¡Carga de ticket promedio completada en PostgreSQL!")
