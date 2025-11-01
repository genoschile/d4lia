from asyncpg import PostgresError
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from itsdangerous import BadSignature, SignatureExpired
from app.config.config import TEMPLATES, serializer
import time

from app.helpers.responses.response import error_response, success_response
from app.instance import get_encuesta_services
from app.schemas.encuesta_schema import GenerarLinkSchema
from app.use_case.encuesta_service import EncuestaService

router = APIRouter(prefix="/encuesta", tags=["Encuesta"])

# {token: timestamp_uso}
tokens_usados = {}

# Tiempo de expiración en segundos (ej. 1 día)
TOKEN_EXPIRACION = 86400  # 24 horas


@router.get("/", response_class=HTMLResponse)
def mostrar_encuesta(request: Request, token: str):
    if token in tokens_usados:
        return HTMLResponse("<h3>Este link ya fue usado</h3>", status_code=400)

    try:
        datos = serializer.loads(token, max_age=TOKEN_EXPIRACION)
    except SignatureExpired:
        return HTMLResponse("<h3>El link ha expirado</h3>", status_code=400)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    return TEMPLATES.TemplateResponse(
        "encuesta.html", {"request": request, "token": token}
    )


@router.post("/generar-link")
async def generar_link(
    request: Request,
    data: GenerarLinkSchema,
    encuesta_service: EncuestaService = Depends(get_encuesta_services),
):

    try:
        token = await encuesta_service.create_link(data.paciente_id, data.sesion_id)
        base_url = str(request.url_for("mostrar_encuesta"))
        link = f"{base_url}?token={token}"

        if not token:
            return error_response(status_code=400, message="No se pudo crear el link.")

        return success_response(
            data=link,
            message="Link creado correctamente",
        )

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


@router.post("/")
async def procesar_encuesta(request: Request):
    data = await request.json()
    token = data.get("token")
    satisfaccion = data.get("satisfaccion")

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

    print(f"Respuesta de paciente {paciente_id}, cita {cita_id}: {satisfaccion}")

    tokens_usados[token] = time.time()

    return JSONResponse(
        {
            "message": "Recibido",
            "paciente_id": paciente_id,
            "cita_id": cita_id,
            "satisfaccion": satisfaccion,
        }
    )
