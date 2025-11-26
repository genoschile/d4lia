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
from app.helpers.response import error_response, success_response
from app.modules.paciente.schemas.paciente_schema import PacienteCreate, PacienteResponse

# -------------------- Router de Pacientes --------------------
router = APIRouter(prefix="/diagnosticos", tags=["Diagnósticos"])


# Crear diagnóstico en una consulta
@router.post("/", response_model=PacienteResponse)
async def crear_diagnostico(
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


# Listar diagnósticos de una consulta
@router.get("/consulta/{id_consulta}", response_model=list[PacienteResponse])
async def listar_diagnosticos_consulta(
    id_consulta: int, paciente_service=Depends(get_paciente_services)
):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar diagnósticos de un paciente (via consultas)
@router.get("/paciente/{id_paciente}", response_model=list[PacienteResponse])
async def listar_diagnosticos_paciente(
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


# Obtener diagnóstico
@router.get("/{id}", response_model=PacienteResponse)
async def obtener_diagnostico(id: int, paciente_service=Depends(get_paciente_services)):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Actualizar diagnóstico
@router.put("/{id}", response_model=PacienteResponse)
async def actualizar_diagnostico(
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


# Eliminar diagnóstico
@router.delete("/{id}", response_model=dict)
async def eliminar_diagnostico(
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


# Buscar diagnósticos por CIE10
@router.get("/buscar/", response_model=list[PacienteResponse])
async def buscar_diagnosticos(
    cie10: str = "",
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
