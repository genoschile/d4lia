from fastapi import APIRouter, Depends
from app.core.exceptions import NotImplementedException
from app.core.instance import get_condicion_personal_services
from app.helpers.responses.response import error_response, success_response
from app.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalResponse,
    CondicionPersonalUpdateRequest,
    PacienteCondicionBase,
    PacienteCondicionResponse,
)
from app.use_case.condicion_personal_service import CondicionPersonalService


router = APIRouter(prefix="/condiciones", tags=["Condiciones Personales"])



# Asociar una condición a un paciente
@router.post("/paciente/{id_paciente}", response_model=PacienteCondicionResponse)
async def asociar_condicion(
    id_paciente: int,
    condicion: PacienteCondicionBase,
    condicion_personal_service: CondicionPersonalService = Depends(get_condicion_personal_services)
):
    nueva = await condicion_personal_service.asociar_condicion_a_paciente(
        id_paciente, condicion
    )

    return success_response(
        data=[PacienteCondicionResponse.from_entity(nueva)],
        message="Condición asociada correctamente al paciente"
    )

# Listar condiciones de un paciente
@router.get("/paciente/{id_paciente}", response_model=list[PacienteCondicionResponse])
def listar_condiciones_paciente(id_paciente: int):
    raise NotImplementedException(
        "Listado de condiciones de paciente aún no implementada"
    )


# Obtener detalle de una condición específica del paciente
@router.get(
    "/paciente/{id_paciente}/condicion/{id_condicion}",
    response_model=PacienteCondicionResponse,
)
def obtener_detalle_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Detalle de condición de paciente aún no implementada"
    )


# Actualizar la condición del paciente
@router.put(
    "/paciente/{id_paciente}/condicion/{id_condicion}",
    response_model=PacienteCondicionResponse,
)
def actualizar_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Actualización de condición de paciente aún no implementada"
    )


# Remover una condición del paciente
@router.delete("/paciente/{id_paciente}/condicion/{id_condicion}", response_model=dict)
def remover_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Remoción de condición de paciente aún no implementada"
    )


# Validar una condición por un médico
@router.post(
    "/paciente/{id_paciente}/condicion/{id_condicion}/validar",
    response_model=PacienteCondicionResponse,
)
def validar_condicion_paciente(id_paciente: int, id_condicion: int):
    raise NotImplementedException(
        "Validación de condición de paciente aún no implementada"
    )
