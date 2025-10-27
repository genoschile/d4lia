import json
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from app.config.config import TEMPLATES

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

## dashboard en tiempo real con WebSockets
respuestas = []
connections = []


async def notificar_todos(data):
    """Notifica a todos los websockets conectados con el nuevo dato."""
    for conn in connections:
        await conn.send_text(json.dumps(data))


# ---------- DASHBOARD ----------
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    conteo = {r: respuestas.count(r) for r in ["excelente", "buena", "regular", "mala"]}
    return TEMPLATES.TemplateResponse(
        "dashboard.html", {"request": request, "conteo": conteo}
    )


@router.websocket("/ws/dashboard")
async def ws_dashboard(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        connections.remove(ws)
