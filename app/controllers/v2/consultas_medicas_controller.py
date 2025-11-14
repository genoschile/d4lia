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
from app.core.instance import get_paciente_services
from app.helpers.responses.response import error_response, success_response
from app.schemas.paciente_schema import PacienteCreate, PacienteResponse

# -------------------- Router de Pacientes --------------------
router = APIRouter(prefix="/consultas_medicas", tags=["Consultas Médicas"])


# Crear consulta para un paciente
@router.post("/", response_model=PacienteResponse)
async def crear_consulta_medica(
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


# Obtener consulta por ID
@router.get("/{id}", response_model=PacienteResponse)
async def obtener_consulta_medica(
    id: int, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar consultas del paciente
@router.get("/paciente/{id_paciente}", response_model=list[PacienteResponse])
async def listar_consultas_paciente(
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


# Actualizar consulta médica
@router.put("/{id}", response_model=PacienteResponse)
async def actualizar_consulta_medica(
    id: int,
    paciente: PacienteCreate,
    paciente_service=Depends(get_paciente_services),
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Eliminar consulta médica
@router.delete("/{id}", response_model=dict)
async def eliminar_consulta_medica(
    id: int, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
