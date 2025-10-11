import json
from typing import Union
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.database import close_db_connection, connect_to_db
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db_connection()


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = "super_secreto"
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generar_token(paciente_id: int, cita_id: int):
    return serializer.dumps({"paciente_id": paciente_id, "cita_id": cita_id})


@app.get("/encuesta", response_class=HTMLResponse)
def mostrar_encuesta(request: Request, token: str):
    try:
        datos = serializer.loads(token, max_age=60 * 60 * 24)
    except SignatureExpired:
        return HTMLResponse("<h3>El enlace ha expirado</h3>", status_code=401)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    return templates.TemplateResponse(
        "encuesta.html", {"request": request, "token": token}
    )


@app.post("/encuesta")
def procesar_encuesta(token: str = Form(...), satisfaccion: str = Form(...)):
    try:
        datos = serializer.loads(token, max_age=60 * 60 * 24)
    except SignatureExpired:
        return HTMLResponse("<h3>El enlace ha expirado</h3>", status_code=401)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    paciente_id = datos["paciente_id"]
    cita_id = datos["cita_id"]

    # Guardar en la base de datos aquí
    print(f"Respuesta de paciente {paciente_id}, cita {cita_id}: {satisfaccion}")

    return RedirectResponse("/gracias", status_code=303)


@app.get("/gracias", response_class=HTMLResponse)
def pagina_gracias(request: Request):
    return templates.TemplateResponse("gracias.html", {"request": request})


## dashboard en tiempo real con WebSockets
respuestas = []
connections = []


async def notificar_todos(data):
    """Notifica a todos los websockets conectados con el nuevo dato."""
    for conn in connections:
        await conn.send_text(json.dumps(data))


# ---------- DASHBOARD ----------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    conteo = {r: respuestas.count(r) for r in ["excelente", "buena", "regular", "mala"]}
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "conteo": conteo}
    )


@app.websocket("/ws/dashboard")
async def ws_dashboard(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        connections.remove(ws)
