import requests
import random
import time
from datetime import datetime

# Tres servicios con su token
SERVICIOS = [
    {"nombre": "auth-service",    "token": "token-alpha-001"},
    {"nombre": "payment-service", "token": "token-beta-002"},
    {"nombre": "meme-ranker",     "token": "token-gamma-003"},
]

MENSAJES = [
    ("INFO",  "Usuario logueado correctamente"),
    ("ERROR", "Timeout al conectar con la base de datos"),
    ("DEBUG", "Consultando base de datos..."),
]

# Loop infinito — manda un log cada 2 segundos
while True:
    servicio = random.choice(SERVICIOS)
    nivel, mensaje = random.choice(MENSAJES)

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service":   servicio["nombre"],
        "severity":  nivel,
        "message":   mensaje,
    }

    respuesta = requests.post(
        "http://localhost:5000/logs",
        json=log,
        headers={"Authorization": f"Token {servicio['token']}"}
    )

    print(f"[{servicio['nombre']}] {nivel} → {respuesta.status_code}")
    time.sleep(2)