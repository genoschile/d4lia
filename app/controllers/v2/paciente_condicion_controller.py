from fastapi import APIRouter, Depends
from app.core.exceptions import NotImplementedException
from app.core.instance import get_paciente_condicion_services
from app.helpers.responses.response import success_response
from app.schemas.condicion_schema import (
    AsociarCondicionPacienteRequest,
    PacienteConCondicionesResponse,
    PacienteCondicionResponse,
)
from app.use_case.condicion_personal_service import CondicionPersonalService
from app.use_case.paciente_condicion_service import PacienteCondicionService


router = APIRouter(prefix="/condiciones", tags=["Condiciones Personales"])


@router.get("/pacienteslist")
async def listar_pacientes_con_condiciones(
    paciente_condicion_service=Depends(get_paciente_condicion_services),
):
    pacientes = await paciente_condicion_service.get_pacientes_con_condiciones()

    return success_response(
        data=[p.model_dump(mode="json") for p in pacientes],
        message="Pacientes y condiciones obtenidos correctamente",
    )


# Asociar una condición a un paciente
@router.post(
    "/paciente/{id_paciente:int}/condicion", response_model=PacienteCondicionResponse
)
async def asociar_condicion(
    id_paciente: int,
    condicion: AsociarCondicionPacienteRequest,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    nueva = await paciente_condicion_service.asociar_condicion_a_paciente(
        id_paciente, condicion
    )

    return success_response(
        data=[PacienteCondicionResponse.from_entity(nueva)],
        message="Condición asociada correctamente al paciente",
    )


@router.get(
    "/paciente/{id_paciente:int}/condiciones",
    response_model=list[PacienteCondicionResponse],
)
def listar_condiciones_paciente(id_paciente: int):
    raise NotImplementedException(
        "Listado de condiciones de paciente aún no implementada"
    )


# Obtener detalle de una condición específica del paciente
@router.get(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}",
    response_model=PacienteCondicionResponse,
)
def obtener_detalle_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Detalle de condición de paciente aún no implementada"
    )


# Actualizar la condición del paciente
@router.put(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}",
    response_model=PacienteCondicionResponse,
)
def actualizar_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Actualización de condición de paciente aún no implementada"
    )


# Remover una condición del paciente
@router.delete("/paciente/{id_paciente:int}/condicion/{id_condicion:int}", response_model=dict)
def remover_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Remoción de condición de paciente aún no implementada"
    )


# Validar una condición por un médico
@router.post(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}/validar",
    response_model=PacienteCondicionResponse,
)
def validar_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Validación de condición de paciente aún no implementada"
    )
