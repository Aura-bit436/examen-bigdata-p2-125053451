import os
import psycopg2

conexion = psycopg2.connect(
    host="db",
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=5432
)

cursor = conexion.cursor()

with open("/tmp/part-00000", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        clave, ingreso = linea.strip().split("\t")
        categoria, mes = clave.split("|")

        cursor.execute("""
            INSERT INTO resultados (clave, categoria, mes, ingreso_total)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (clave) DO UPDATE
            SET categoria = EXCLUDED.categoria,
                mes = EXCLUDED.mes,
                ingreso_total = EXCLUDED.ingreso_total
        """, (clave, categoria, mes, ingreso))

conexion.commit()
print("Resultados cargados correctamente:", cursor.rowcount)

cursor.close()
conexion.close()