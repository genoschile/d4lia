from fastapi import APIRouter, Depends
from app.core.exceptions import NotImplementedException
from app.core.instance import (
    get_condicion_personal_services,
    get_paciente_condicion_services,
)
from app.helpers.response import error_response, success_response
from app.modules.paciente_condicion.schemas.condicion_schema import (
    AsociarCondicionPacienteRequest,
    PacienteConCondicionesResponse,
    PacienteCondicionResponse,
    PacienteCondicionUpdate,
)

from app.modules.paciente_condicion.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalResponse,
    CondicionPersonalUpdateRequest,
    PacienteCondicionBase,
    PacienteCondicionResponse,
)
from app.modules.paciente_condicion.services.condicion_personal_service import (
    CondicionPersonalService,
)
from app.modules.paciente_condicion.services.paciente_condicion_service import (
    PacienteCondicionService,
)


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
async def listar_condiciones_paciente(
    id_paciente: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    condiciones = await paciente_condicion_service.listar_condiciones_de_paciente(
        id_paciente
    )
    return success_response(
        data=[PacienteCondicionResponse.from_entity(c) for c in condiciones],
        message="Condiciones del paciente obtenidas correctamente",
    )


# Obtener detalle de una condición específica del paciente
@router.get(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}",
    response_model=PacienteCondicionResponse,
)
async def obtener_detalle_condicion_paciente(
    id_paciente: int,
    id_condicion: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    details_condition = (
        await paciente_condicion_service.obtener_detalle_condicion_paciente(
            id_paciente, id_condicion
        )
    )

    return success_response(
        data=[PacienteCondicionResponse.from_entity(details_condition)],
        message="Detalle de la condición del paciente obtenido correctamente",
    )


@router.patch(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}",
    response_model=PacienteCondicionResponse,
)
async def actualizar_condicion_paciente(
    id_paciente: int,
    id_condicion: int,
    payload: PacienteCondicionUpdate,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    condicion_actualizada = (
        await paciente_condicion_service.actualizar_condicion_de_paciente(
            id_paciente=id_paciente,
            id_condicion=id_condicion,
            data=payload,
        )
    )

    return success_response(
        data=PacienteCondicionResponse.from_entity(condicion_actualizada),
        message="Condición del paciente actualizada correctamente",
    )


@router.delete(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}",
    response_model=dict,
)
async def remover_condicion_paciente(
    id_paciente: int,
    id_condicion: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    await paciente_condicion_service.remover_condicion_de_paciente(
        id_paciente,
        id_condicion,
    )

    return success_response(
        data={},
        message="Condición del paciente removida correctamente",
    )


# Validate condition by doctor
@router.patch(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}/validar",
    response_model=PacienteCondicionResponse,
)
async def validar_condicion_paciente(
    id_paciente: int,
    id_condicion: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    condicion = await paciente_condicion_service.validar_condicion(
        id_paciente,
        id_condicion,
    )

    return success_response(
        message="Condición validada correctamente",
        data=PacienteCondicionResponse.from_entity(condicion),
    )


@router.patch(
    "/paciente/{id_paciente:int}/condicion/{id_condicion:int}/invalidar",
    response_model=PacienteCondicionResponse,
)
async def invalidar_condicion_paciente(
    id_paciente: int,
    id_condicion: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    condicion = await paciente_condicion_service.invalidar_condicion(
        id_paciente, id_condicion
    )

    return success_response(
        message="Condición invalidada correctamente",
        data=PacienteCondicionResponse.from_entity(condicion),
    )


@router.get(
    "/paciente/{id_paciente:int}/condiciones/validadas",
    response_model=list[PacienteCondicionResponse],
)
async def listar_condiciones_validadas(
    id_paciente: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    condiciones = await paciente_condicion_service.listar_condiciones_validadas(
        id_paciente
    )

    return success_response(
        message="Condiciones validadas obtenidas correctamente",
        data=[PacienteCondicionResponse.from_entity(c) for c in condiciones],
    )


@router.get(
    "/paciente/{id_paciente:int}/condiciones/no-validadas",
    response_model=list[PacienteCondicionResponse],
)
async def listar_condiciones_no_validadas(
    id_paciente: int,
    paciente_condicion_service: PacienteCondicionService = Depends(
        get_paciente_condicion_services
    ),
):
    condiciones = await paciente_condicion_service.listar_condiciones_no_validadas(
        id_paciente
    )

    return success_response(
        message="Condiciones no validadas obtenidas correctamente",
        data=[PacienteCondicionResponse.from_entity(c) for c in condiciones],
    )


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

    if not condicion_personal_new:
        return error_response(
            message="Error al crear la condición personal", status_code=500
        )

    return success_response(
        data=[
            CondicionPersonalResponse.from_entity(entidad)
            for entidad in [condicion_personal_new]
        ],
        message="Condición personal creada correctamente",
    )


# Obtener una condición por ID
@router.get("/{id:int}", response_model=CondicionPersonalResponse)
async def obtener_condicion(
    id: int,
    condicion_personal_service: CondicionPersonalService = Depends(
        get_condicion_personal_services
    ),
):
    search_result = await condicion_personal_service.get_condicion_personal_by_id(id)

    if not search_result:
        return error_response(
            message="Condición personal no encontrada", status_code=404
        )

    return success_response(
        data=[CondicionPersonalResponse.from_entity(search_result)],
        message="Condición personal obtenida correctamente",
    )


# Listar todas las condiciones registradas
@router.get("/", response_model=list[CondicionPersonalResponse])
async def listar_condiciones(
    condicion_personal_service: CondicionPersonalService = Depends(
        get_condicion_personal_services
    ),
):
    list_condiciones = (
        await condicion_personal_service.list_all_condiciones_personales()
    )

    return success_response(
        data=[
            CondicionPersonalResponse.from_entity(entidad)
            for entidad in list_condiciones
        ],
        message="Listado de condiciones personales obtenido correctamente",
    )


# Actualizar una condición existente
@router.patch("/{id:int}", response_model=CondicionPersonalResponse)
async def actualizar_condicion(
    id: int,
    payload: CondicionPersonalUpdateRequest,
    condicion_personal_service: CondicionPersonalService = Depends(
        get_condicion_personal_services
    ),
):
    updated = await condicion_personal_service.update_condicion_personal(id, payload)

    return success_response(
        data=[CondicionPersonalResponse.from_entity(updated)],
        message="Condición personal actualizada correctamente",
    )


# Eliminar una condición por ID
@router.delete("/{id:int}")
async def eliminar_condicion(
    id: int,
    condicion_personal_service: CondicionPersonalService = Depends(
        get_condicion_personal_services
    ),
):

    await condicion_personal_service.delete_condicion_personal(id)

    return success_response(
        message="Condición personal eliminada correctamente", data=None
    )


@router.get("/buscar/", response_model=list[CondicionPersonalResponse])
async def buscar_condiciones(
    codigo: str = "",
    nombre: str = "",
    condicion_personal_service: CondicionPersonalService = Depends(
        get_condicion_personal_services
    ),
):

    resultados = await condicion_personal_service.buscar_condiciones(codigo, nombre)

    return success_response(
        data=[CondicionPersonalResponse.from_entity(r) for r in resultados],
        message="Resultados de la búsqueda obtenidos correctamente",
    )
