
import os
import time
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def conectar():
    return psycopg2.connect(
        host="db",
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432
    )

def inicializar_bd():
    for intento in range(30):
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultados (
                    clave VARCHAR(150) PRIMARY KEY,
                    categoria VARCHAR(100) NOT NULL,
                    mes VARCHAR(7) NOT NULL,
                    ingreso_total NUMERIC(16,2) NOT NULL
                )
            """)
            conexion.commit()
            cursor.close()
            conexion.close()
            print("Base de datos preparada")
            return
        except psycopg2.OperationalError:
            print("Esperando PostgreSQL...")
            time.sleep(2)
    raise Exception("No fue posible conectar con PostgreSQL")

@app.route("/resultados", methods=["GET"])
def obtener_resultados():
    conexion = conectar()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM resultados ORDER BY mes, categoria")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(datos)

@app.route("/resultados/<string:clave>", methods=["GET"])
def obtener_resultado(clave):
    conexion = conectar()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM resultados WHERE clave = %s", (clave,))
    dato = cursor.fetchone()
    cursor.close()
    conexion.close()
    if dato is None:
        return jsonify({"error": "Resultado no encontrado"}), 404
    return jsonify(dato)

@app.route("/resultados", methods=["POST"])
def crear_resultado():
    datos = request.get_json()
    if not datos or not all(k in datos for k in ("clave", "categoria", "mes", "ingreso_total")):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO resultados (clave, categoria, mes, ingreso_total)
            VALUES (%s, %s, %s, %s)
        """, (datos["clave"], datos["categoria"], datos["mes"], datos["ingreso_total"]))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "Resultado creado"}), 201
    except psycopg2.IntegrityError:
        conexion.rollback()
        conexion.close()
        return jsonify({"error": "La clave ya existe"}), 409

@app.route("/resultados/<string:clave>", methods=["PUT"])
def actualizar_resultado(clave):
    datos = request.get_json()
    if not datos or not all(k in datos for k in ("categoria", "mes", "ingreso_total")):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE resultados
        SET categoria=%s, mes=%s, ingreso_total=%s
        WHERE clave=%s
    """, (datos["categoria"], datos["mes"], datos["ingreso_total"], clave))
    actualizado = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    if not actualizado:
        return jsonify({"error": "Resultado no encontrado"}), 404
    return jsonify({"mensaje": "Resultado actualizado"})

@app.route("/resultados/<string:clave>", methods=["DELETE"])
def eliminar_resultado(clave):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM resultados WHERE clave=%s", (clave,))
    eliminado = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    if not eliminado:
        return jsonify({"error": "Resultado no encontrado"}), 404
    return jsonify({"mensaje": "Resultado eliminado"})

if __name__ == "__main__":
    inicializar_bd()
    app.run(host="0.0.0.0", port=5000)
