# CIE10 – Catálogo de enfermedades
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
router = APIRouter(prefix="/CIE10", tags=["CIE10"])

# Listar CIE10
@router.get("/", response_model=list[PacienteResponse])
async def listar_cie10(paciente_service=Depends(get_paciente_services)):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
    
# Buscar por código o nombre
@router.get("/buscar/", response_model=list[PacienteResponse])
async def buscar_cie10(codigo: str = "", nombre: str = "", paciente_service=Depends(get_paciente_services)):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
    

# Obtener enfermedad por código
@router.get("/{codigo}", response_model=PacienteResponse)
async def obtener_cie10(codigo: str, paciente_service=Depends(get_paciente_services)):
    try:
        pass
    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")