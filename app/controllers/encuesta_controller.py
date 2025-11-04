from asyncpg import PostgresError
from fastapi import APIRouter, Depends, Request
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
    """Muestra la encuesta según el token y tipo."""
    if token in tokens_usados:
        return HTMLResponse("<h3>Este link ya fue usado</h3>", status_code=400)

    try:
        datos = serializer.loads(token, max_age=TOKEN_EXPIRACION)
    except SignatureExpired:
        return HTMLResponse("<h3>El link ha expirado</h3>", status_code=400)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    tipo_encuesta = datos.get("tipo_encuesta", "satisfaccion")

    return TEMPLATES.TemplateResponse(
        "encuesta.html",
        {"request": request, "token": token, "tipo_encuesta": tipo_encuesta},
    )


@router.post("/generar-link")
async def generar_link(
    request: Request,
    data: GenerarLinkSchema,
    encuesta_service: EncuestaService = Depends(get_encuesta_services),
):
    """Genera un link único firmado para una sesión, paciente y tipo_encuesta."""
    try:
        # Ahora incluimos el tipo_encuesta dentro del token
        payload = {
            "paciente_id": data.paciente_id,
            "sesion_id": data.sesion_id,
            "tipo_encuesta": data.tipo_encuesta.value,
        }
        token = serializer.dumps(payload)

        base_url = str(request.url_for("mostrar_encuesta"))
        link = f"{base_url}?token={token}"

        return success_response(
            data={"link": link, "tipo_encuesta": data.tipo_encuesta.value},
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
    """Recibe y valida una encuesta enviada, sin persistirla."""
    data = await request.json()
    token = data.get("token")
    respuestas = data.get("respuestas")

    if token in tokens_usados:
        return JSONResponse({"error": "Este link ya fue usado"}, status_code=400)

    try:
        datos = serializer.loads(token, max_age=TOKEN_EXPIRACION)
    except SignatureExpired:
        return JSONResponse({"error": "El link ha expirado"}, status_code=400)
    except BadSignature:
        return JSONResponse({"error": "Token inválido"}, status_code=400)

    paciente_id = datos["paciente_id"]
    sesion_id = datos["sesion_id"]
    tipo_encuesta = datos["tipo_encuesta"]

    print(f"[Encuesta {tipo_encuesta}] Paciente {paciente_id}, Sesión {sesion_id}")
    print(f"Respuestas: {respuestas}")

    tokens_usados[token] = time.time()

    return JSONResponse(
        {
            "message": f"Encuesta {tipo_encuesta} recibida correctamente.",
            "paciente_id": paciente_id,
            "sesion_id": sesion_id,
            "tipo_encuesta": tipo_encuesta,
            "respuestas": respuestas,
        }
    )
