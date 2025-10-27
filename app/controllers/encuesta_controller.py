from typing import Union
from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database.database import close_db_connection, connect_to_db
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
from app.config.config import TEMPLATES
from app.use_case.welcome_service import WelcomeService
from app.config.config import serializer
router = APIRouter(prefix="/encuesta", tags=["Encuesta"])


@router.get("/", response_class=HTMLResponse)
def mostrar_encuesta(request: Request, token: str):
    try:
        datos = serializer.loads(token, max_age=60 * 60 * 24)
    except SignatureExpired:
        return HTMLResponse("<h3>El enlace ha expirado</h3>", status_code=401)
    except BadSignature:
        return HTMLResponse("<h3>Token inválido</h3>", status_code=400)

    return TEMPLATES.TemplateResponse(
        "encuesta.html", {"request": request, "token": token}
    )


@router.post("/")
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
