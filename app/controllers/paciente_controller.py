from asyncpg import PostgresError
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
import httpx
from app.config.config import TEMPLATES
from app.domain.paciente_entity import Paciente
from app.helpers.responses.response import error_response, success_response
from app.instance import get_paciente_services
from app.schemas.paciente_schema import PacienteCreate, PacienteResponse
from dataclasses import asdict


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


# ----------- FORMULARIO PARA AGREGAR PACIENTE -----------
@router.get("/add", response_class=HTMLResponse)
async def add_paciente_form(request: Request):
    return TEMPLATES.TemplateResponse("add_paciente.html", {"request": request})


# ----------- LISTAR SILLONES -----------
@router.get("/", response_model=list[PacienteResponse])
async def listar_pacientes(paciente_service=Depends(get_paciente_services)):
    try:
        pacientes = await paciente_service.get_all_pacientes()
        paciente_response = [
            PacienteResponse.model_validate(asdict(p)) for p in pacientes
        ]

        return success_response(
            data=[s.model_dump(mode="json") for s in paciente_response],
            message="Pacientes obtenidos correctamente",
        )

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- CREAR PACIENTE -----------
@router.post("/", response_model=PacienteResponse)
async def create_paciente(
    paciente: PacienteCreate, paciente_service=Depends(get_paciente_services)
):
    try:
        nuevo_paciente = await paciente_service.create_paciente(paciente)
        paciente_dict = {
            "id_paciente": nuevo_paciente.id_paciente,
            "nombre_completo": nuevo_paciente.nombre_completo,
            "correo": nuevo_paciente.correo,
            "telefono": nuevo_paciente.telefono,
            "edad": nuevo_paciente.edad,
            "fecha_inicio_tratamiento": nuevo_paciente.fecha_inicio_tratamiento,
            "observaciones": nuevo_paciente.observaciones,
        }
        return success_response(
            data=PacienteResponse(**paciente_dict),
            message="Paciente creado correctamente y webhook notificado",
        )
    except httpx.HTTPStatusError as e:
        return error_response(status_code=500, message=f"Webhook falló: {str(e)}")
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
