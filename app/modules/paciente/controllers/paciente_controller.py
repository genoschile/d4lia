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

# -------------------- Router de Pacientes --------------------
router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


# ----------- FORMULARIO PARA AGREGAR PACIENTE -----------
@router.get("/add", response_class=HTMLResponse)
async def add_paciente_form(request: Request):
    return TEMPLATES.TemplateResponse("add_paciente.html", {"request": request})


# ----------- LISTAR PACIENTE -----------
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
            "rut": nuevo_paciente.rut,
            "nombre_completo": nuevo_paciente.nombre_completo,
            "correo": nuevo_paciente.correo,
            "telefono": nuevo_paciente.telefono,
            "edad": nuevo_paciente.edad,
            "fecha_inicio_tratamiento": nuevo_paciente.fecha_inicio_tratamiento,
            "observaciones": nuevo_paciente.observaciones,
        }
        return success_response(
            data=PacienteResponse(**paciente_dict).model_dump(),
            message=f"Paciente creado correctamente MODE: {settings.ENV}",
        )

    except asyncpg.UniqueViolationError as e:
        return error_response(
            status_code=409,  # 409 Conflict
            message=f"El RUT '{paciente.rut}' ya está registrado.",
        )

    except asyncpg.CheckViolationError:
        return error_response(
            status_code=400,
            message="La edad del paciente debe ser mayor a 0.",
        )
    except httpx.HTTPStatusError as e:
        return error_response(status_code=500, message=f"Webhook falló: {str(e)}")
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# ----------- DELETE PACIENTE -----------
@router.delete("/{id_paciente:int}", response_model=PacienteResponse)
async def delete_paciente(
    id_paciente: int, paciente_service=Depends(get_paciente_services)
):
    try:
        eliminado = await paciente_service.delete_paciente(id_paciente)
        if not eliminado:
            return error_response(
                status_code=404, message=f"Paciente con ID {id_paciente} no encontrado."
            )
        return success_response(
            data={"id_paciente": id_paciente},
            message="Paciente eliminado correctamente.",
        )

    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
    
# Editar paciente
@router.put("/{id_paciente:int}", response_model=PacienteResponse)
async def update_paciente(
    id_paciente: int,
    paciente: PacienteCreate,
    paciente_service=Depends(get_paciente_services),
):
    try:
        actualizado = await paciente_service.update_paciente(id_paciente, paciente)
        if not actualizado:
            return error_response(
                status_code=404, message=f"Paciente con ID {id_paciente} no encontrado."
            )
        paciente_dict = {
            "id_paciente": actualizado.id_paciente,
            "rut": actualizado.rut,
            "nombre_completo": actualizado.nombre_completo,
            "correo": actualizado.correo,
            "telefono": actualizado.telefono,
            "edad": actualizado.edad,
            "fecha_inicio_tratamiento": actualizado.fecha_inicio_tratamiento,
            "observaciones": actualizado.observaciones,
        }
        return success_response(
            data=PacienteResponse(**paciente_dict).model_dump(),
            message="Paciente actualizado correctamente.",
        )

    except asyncpg.UniqueViolationError as e:
        return error_response(
            status_code=409,  # 409 Conflict
            message=f"El RUT '{paciente.rut}' ya está registrado.",
        )

    except asyncpg.CheckViolationError:
        return error_response(
            status_code=400,
            message="La edad del paciente debe ser mayor a 0.",
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
    

# Buscar por RUT, nombre o teléfono
@router.get("/buscar/", response_model=list[PacienteResponse])
async def buscar_pacientes(
    rut: str = "",
    nombre: str = "",
    telefono: str = "",
    paciente_service=Depends(get_paciente_services),
):
    try:
        pacientes = await paciente_service.search_pacientes(rut, nombre, telefono)
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
    

# Obtener historial completo del paciente (mega endpoint)
@router.get("/{id_paciente:int}/historial", response_model=PacienteResponse)
async def obtener_historial_paciente(
    id_paciente: int, paciente_service=Depends(get_paciente_services)
):
    try:
        historial = await paciente_service.get_paciente_historial(id_paciente)
        if not historial:
            return error_response(
                status_code=404, message=f"Paciente con ID {id_paciente} no encontrado."
            )

        paciente_dict = {
            "id_paciente": historial.id_paciente,
            "rut": historial.rut,
            "nombre_completo": historial.nombre_completo,
            "correo": historial.correo,
            "telefono": historial.telefono,
            "edad": historial.edad,
            "fecha_inicio_tratamiento": historial.fecha_inicio_tratamiento,
            "observaciones": historial.observaciones,
            # Aquí se podrían agregar más detalles del historial si es necesario
        }

        return success_response(
            data=PacienteResponse(**paciente_dict).model_dump(),
            message="Historial del paciente obtenido correctamente.",
        )

    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")