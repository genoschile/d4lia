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
