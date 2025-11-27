from fastapi import APIRouter, Depends
from app.modules.orden_examen.schemas.orden_examen_schema import (
    OrdenExamenResponse,
    OrdenExamenCreate,
    OrdenExamenUpdate,
)
from app.modules.orden_examen.services.orden_examen_service import OrdenExamenService
from app.modules.instance import get_orden_examen_service
from app.helpers.response import success_response

router = APIRouter(prefix="/orden_examen", tags=["Orden de Examen"])


@router.get("/", response_model=list[OrdenExamenResponse])
async def listar_ordenes(
    service: OrdenExamenService = Depends(get_orden_examen_service),
):
    """Listar todas las órdenes de examen"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Órdenes listadas correctamente",
    )


@router.post("/", response_model=OrdenExamenResponse)
async def crear_orden(
    data: OrdenExamenCreate,
    service: OrdenExamenService = Depends(get_orden_examen_service),
):
    """Crear una nueva orden de examen"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Orden creada correctamente"
    )


@router.get("/{id}", response_model=OrdenExamenResponse)
async def obtener_orden(
    id: int, service: OrdenExamenService = Depends(get_orden_examen_service)
):
    """Obtener una orden por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Orden obtenida correctamente"
    )


@router.patch("/{id}", response_model=OrdenExamenResponse)
async def actualizar_orden(
    id: int,
    data: OrdenExamenUpdate,
    service: OrdenExamenService = Depends(get_orden_examen_service),
):
    """Actualizar una orden de examen"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Orden actualizada correctamente"
    )


@router.delete("/{id}")
async def eliminar_orden(
    id: int, service: OrdenExamenService = Depends(get_orden_examen_service)
):
    """Eliminar una orden de examen"""
    await service.delete(id)
    return success_response(message="Orden eliminada correctamente")


@router.get("/paciente/{id_paciente}", response_model=list[OrdenExamenResponse])
async def listar_por_paciente(
    id_paciente: int,
    service: OrdenExamenService = Depends(get_orden_examen_service),
):
    """Listar órdenes de un paciente"""
    items = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Órdenes del paciente listadas correctamente",
    )


@router.get("/consulta/{id_consulta}", response_model=list[OrdenExamenResponse])
async def listar_por_consulta(
    id_consulta: int,
    service: OrdenExamenService = Depends(get_orden_examen_service),
):
    """Listar órdenes de una consulta médica"""
    items = await service.get_by_consulta(id_consulta)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Órdenes de la consulta listadas correctamente",
    )
