# Primero importamos Flask para crear el servidor
from flask import Flask, request, jsonify
# sqlite3 para crear nuestra base de datos
import sqlite3
import datetime

app = Flask(__name__)

# Definimos la lista de Tokens validos
TOKENS= ["token-alpha-001", "token-beta-002", "token-gamma-003"]

# Funcion para crear la base de datos y si no existe el archivo logs se crea
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

@app.route("/logs", methods=["POST"])
def recibir_log():
    