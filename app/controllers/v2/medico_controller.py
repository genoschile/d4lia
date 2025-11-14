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


router = APIRouter(prefix="/medico", tags=["MEDICOS"])


# Listar médicos
@router.get("/", response_model=list)
async def listar_medicos():
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Obtener médico por ID
@router.get("/{id}", response_model=dict)
async def obtener_medico(id: int):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Buscar médicos por especialidad
@router.get("/buscar/", response_model=list)
async def buscar_medicos(especialidad: str):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar especialidades médicas
@router.get("/especialidades/", response_model=list)
async def listar_especialidades():
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar médicos activos
@router.get("/activos/", response_model=list)
async def listar_medicos_activos():
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
    

# Obtener el perfil del médico que atendió a un paciente
@router.get("/perfil/paciente/{id_paciente}", response_model=dict)
async def obtener_perfil_medico_paciente(id_paciente: int):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
    

