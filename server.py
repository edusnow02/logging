from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Tokens válidos
TOKENS = ["token-alpha-001", "token-beta-002", "token-gamma-003"]
  
# Crear la tabla si no existe
def inicializar_db():
    with sqlite3.connect("logs_data/logs.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT,
                service     TEXT,   
                severity    TEXT,
                message     TEXT,
                received_at TEXT
            )
        """)

# Recibir un log
@app.route("/logs", methods=["POST"])
def recibir_log():

    # Verificar token
    token = request.headers.get("Authorization", "").replace("Token ", "")
    if token not in TOKENS:
        return jsonify({"error": "Quién sos, bro?"}), 401

    # Leer el JSON que mandó el cliente
    datos = request.get_json()

    # Guardarlo en la base de datos
    with sqlite3.connect("logs_data/logs.db") as conn:
        conn.execute(
            "INSERT INTO logs (timestamp, service, severity, message, received_at) VALUES (?,?,?,?,?)",
            (datos["timestamp"], datos["service"], datos["severity"], datos["message"], datetime.utcnow().isoformat())
        )

    return jsonify({"mensaje": "Log guardado"}), 201

# Consultar logs
@app.route("/logs", methods=["GET"])
def consultar_logs():
    with sqlite3.connect("logs_data/logs.db") as conn:
        conn.row_factory = sqlite3.Row
        filas = conn.execute("SELECT * FROM logs ORDER BY received_at DESC").fetchall()

    return jsonify({"total": len(filas), "logs": [dict(f) for f in filas]}), 200

if __name__ == "__main__":
    inicializar_db()
    app.run(debug=True, port=5000)