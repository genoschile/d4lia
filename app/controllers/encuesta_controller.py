from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from itsdangerous import BadSignature, SignatureExpired
from pydantic import BaseModel
from app.config.config import TEMPLATES, serializer
import time

router = APIRouter(prefix="/encuesta", tags=["Encuesta"])

# Diccionario para tokens usados: {token: timestamp_uso}
tokens_usados = {}

# Tiempo de expiración en segundos (ej. 1 día)
TOKEN_EXPIRACION = 86400  # 24 horas

# Mostrar encuesta (accede con token)
@router.get("/", response_class=HTMLResponse)
def mostrar_encuesta(request: Request, token: str):
    # Primero verificamos si ya fue usado
    if token in tokens_usados:
        return HTMLResponse("<h3>Este link ya fue usado</h3>", status_code=400)

    try:
        # Intentamos cargar el token con expiración
        datos = serializer.loads(token, max_age=TOKEN_EXPIRACION)
    except SignatureExpired:
        return HTMLResponse("<h3>El link ha expirado</h3>", status_code=400)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    return TEMPLATES.TemplateResponse(
        "encuesta.html", {"request": request, "token": token}
    )


class GenerarLinkSchema(BaseModel):
    paciente_id: int
    cita_id: int


@router.post("/generar-link")
def generar_link(request: Request, data: GenerarLinkSchema):
    token = serializer.dumps({"paciente_id": data.paciente_id, "cita_id": data.cita_id})
    base_url = str(request.url_for("mostrar_encuesta"))
    link = f"{base_url}?token={token}"
    return {"link": link}


@router.post("/")
async def procesar_encuesta(request: Request):
    data = await request.json()
    token = data.get("token")
    satisfaccion = data.get("satisfaccion")

    # Verificamos si ya fue usado
    if token in tokens_usados:
        return JSONResponse({"error": "Este link ya fue usado"}, status_code=400)

    try:
        datos = serializer.loads(token, max_age=TOKEN_EXPIRACION)
    except SignatureExpired:
        return JSONResponse({"error": "El link ha expirado"}, status_code=400)
    except BadSignature:
        return JSONResponse({"error": "Token inválido"}, status_code=400)

    paciente_id = datos["paciente_id"]
    cita_id = datos["cita_id"]

    # Solo imprimir
    print(f"Respuesta de paciente {paciente_id}, cita {cita_id}: {satisfaccion}")

    # Marcar token como usado
    tokens_usados[token] = time.time()

    return JSONResponse(
        {
            "message": "Recibido",
            "paciente_id": paciente_id,
            "cita_id": cita_id,
            "satisfaccion": satisfaccion,
        }
    )
