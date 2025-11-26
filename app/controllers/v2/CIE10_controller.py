# CIE10 – Catálogo de enfermedades
# -------------------- Librerías estándar --------------------
from dataclasses import asdict

# -------------------- Dependencias externas --------------------
import asyncpg
from asyncpg import PostgresError
import httpx
from fastapi import APIRouter, Depends

# -------------------- Configuración del proyecto --------------------
from app.config.config import TEMPLATES
from app.config.environment import settings

# -------------------- Dependencias internas --------------------
from app.core.exceptions import NotImplementedException
from app.core.instance import get_paciente_services
from app.helpers.response import error_response, success_response
from app.modules.paciente.schemas.paciente_schema import PacienteCreate, PacienteResponse

# -------------------- Router de Pacientes --------------------
router = APIRouter(prefix="/CIE10", tags=["CIE10"])


# Listar CIE10
@router.get("/", response_model=list[PacienteResponse])
async def listar_cie10(paciente_service=Depends(get_paciente_services)):

    raise NotImplementedException("Listado de CIE10 aún no implementada")


# Buscar por código o nombre
@router.get("/buscar/", response_model=list[PacienteResponse])
async def buscar_cie10(
    codigo: str = "", nombre: str = "", paciente_service=Depends(get_paciente_services)
):
    raise NotImplementedException(
        "Búsqueda de CIE10 por código o nombre aún no implementada"
    )


# Obtener enfermedad por código
@router.get("/{codigo}", response_model=PacienteResponse)
async def obtener_cie10(codigo: str, paciente_service=Depends(get_paciente_services)):

    raise NotImplementedException(
        "Obtención de enfermedad por código aún no implementada"
    )
