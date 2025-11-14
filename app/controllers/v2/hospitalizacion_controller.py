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


router = APIRouter(prefix="/hospitalizacion", tags=["HOSPITALIZACIONES"])


# Registrar orden de hospitalización
@router.post("/", response_model=PacienteResponse)
async def registrar_hospitalizacion(
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
    

# Registrar ingreso a hospitalización
@router.post("/ingreso/", response_model=PacienteResponse)
async def registrar_ingreso_hospitalizacion(
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
    
# Ver hospitalizaciones del paciente
@router.get("/paciente/{id_paciente}", response_model=list[PacienteResponse])
async def ver_hospitalizaciones_paciente(
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
    

# orden_hospitalizacion

# hospitalizacion

# tratamiento_hospitalizacion

# medicamento_hospitalizacion

# 👉 Falta crear rutas como:

# Crear orden de hospitalización

# Aprobar/activar hospitalización

# Cerrar hospitalización (alta)

# Registrar tratamientos aplicados durante la hospitalización

# Registrar medicamentos aplicados