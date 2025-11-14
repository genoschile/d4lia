from asyncpg import PostgresError
from fastapi import APIRouter, Depends

from app.core.instance import get_condicion_personal_services
from app.helpers.responses.response import error_response, success_response
from app.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalResponse,
    PacienteCondicionBase,
    PacienteCondicionResponse,
)
from app.use_case.condicion_personal_service import CondicionPersonalService


router = APIRouter(prefix="/condiciones", tags=["Condiciones Personales"])


# Crear nueva condición personal
@router.post("/", response_model=CondicionPersonalResponse)
async def crear_condicion(
    condicion_personal: CondicionPersonalCreate,
    condicion_personal_service: CondicionPersonalService = Depends(
        get_condicion_personal_services
    ),
):

    condicion_personal_new = await condicion_personal_service.create_condicion_personal(
        condicion_personal
    )

    return success_response(
        data=[
            CondicionPersonalResponse.from_entity(entidad)
            for entidad in [condicion_personal_new]
        ],
        message="Condición personal creada correctamente",
    )


# Obtener una condición por ID
@router.get("/{id}", response_model=CondicionPersonalResponse)
def obtener_condicion(id: int):
    pass


# Actualizar una condición existente
@router.put("/{id}", response_model=CondicionPersonalResponse)
def actualizar_condicion(id: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Eliminar una condición por ID
@router.delete("/{id}", response_model=dict)
def eliminar_condicion(id: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Buscar por código o nombre
@router.get("/buscar/", response_model=list[CondicionPersonalResponse])
def buscar_condiciones(codigo: str = "", nombre: str = ""):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Asociar una condición a un paciente
@router.post("/paciente/{id_paciente}", response_model=PacienteCondicionResponse)
def asociar_condicion(id_paciente: int, condicion: PacienteCondicionBase):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar todas las condiciones registradas
@router.get("/", response_model=list[PacienteCondicionResponse])
def listar_condiciones():
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Listar condiciones de un paciente
@router.get("/paciente/{id_paciente}", response_model=list[PacienteCondicionResponse])
def listar_condiciones_paciente(id_paciente: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Obtener detalle de una condición específica del paciente
@router.get(
    "/paciente/{id_paciente}/condicion/{id_condicion}",
    response_model=PacienteCondicionResponse,
)
def obtener_detalle_condicion_paciente(id_paciente: int, id_condicion: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Actualizar la condición del paciente
@router.put(
    "/paciente/{id_paciente}/condicion/{id_condicion}",
    response_model=PacienteCondicionResponse,
)
def actualizar_condicion_paciente(id_paciente: int, id_condicion: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Remover una condición del paciente
@router.delete("/paciente/{id_paciente}/condicion/{id_condicion}", response_model=dict)
def remover_condicion_paciente(id_paciente: int, id_condicion: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")


# Validar una condición por un médico
@router.post(
    "/paciente/{id_paciente}/condicion/{id_condicion}/validar",
    response_model=PacienteCondicionResponse,
)
def validar_condicion_paciente(id_paciente: int, id_condicion: int):
    try:
        pass

    except PostgresError as e:
        return error_response(
            status_code=500, message=f"Error en base de datos: {str(e)}"
        )
    except Exception as e:
        return error_response(status_code=500, message=f"Error interno: {str(e)}")
