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

# -------------------- Dependencias internas --------------------
from app.modules.instance import get_paciente_services
from app.helpers.response import error_response, success_response
from app.modules.paciente.schemas.paciente_schema import PacienteCreate, PacienteResponse


router = APIRouter(prefix="/examen-orden", tags=["EXÁMENES Y ÓRDENES DE EXAMEN"])


# Crear orden de examen para un paciente
@router.post("/", response_model=PacienteResponse)
async def crear_orden_examen(
    paciente: PacienteCreate, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar órdenes por paciente
@router.get("/paciente/{id_paciente}", response_model=list[PacienteResponse])
async def listar_ordenes_paciente(
    id_paciente: int, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Subir resultado de examen
@router.post("/resultado/{id_orden}", response_model=PacienteResponse)
async def subir_resultado_examen(
    id_orden: int, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Resultados del paciente
@router.get("/resultados/paciente/{id_paciente}", response_model=list[PacienteResponse])
async def listar_resultados_paciente(
    id_paciente: int, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
