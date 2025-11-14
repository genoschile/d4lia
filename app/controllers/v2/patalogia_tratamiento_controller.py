# -------------------- Librerías estándar --------------------
from dataclasses import asdict

# -------------------- Dependencias externas --------------------
import asyncpg
from asyncpg import PostgresError
import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

# -------------------- Configuración del proyecto --------------------
from app.config.config import TEMPLATES
from app.config.environment import settings
from app.helpers.responses.response import error_response


router = APIRouter(prefix="/patologia-tratamiento", tags=["PATOLOGIA_TRATAMIENTO"])


# Listar todas las patologías y tratamientos
@router.get("/", response_model=list)
async def listar_patologias_tratamientos():
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# CRUD de tratamientos

# Listar tratamientos de una patología
# Asignar tratamiento a patología
# Quitar tratamiento a patología
