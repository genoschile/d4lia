from fastapi import APIRouter, Depends
from app.modules.orden_hospitalizacion.schemas.orden_hospitalizacion_schema import (
    OrdenHospitalizacionResponse,
    OrdenHospitalizacionCreate,
    OrdenHospitalizacionUpdate,
)
from app.modules.orden_hospitalizacion.services.orden_hospitalizacion_service import OrdenHospitalizacionService
from app.modules.instance import get_orden_hospitalizacion_service
from app.helpers.response import success_response

router = APIRouter(prefix="/orden_hospitalizacion", tags=["Orden de Hospitalización"])


@router.get("/", response_model=list[OrdenHospitalizacionResponse])
async def listar_ordenes(
    service: OrdenHospitalizacionService = Depends(get_orden_hospitalizacion_service),
):
    """Listar todas las órdenes de hospitalización"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Órdenes listadas correctamente",
    )


@router.post("/", response_model=OrdenHospitalizacionResponse)
async def crear_orden(
    data: OrdenHospitalizacionCreate,
    service: OrdenHospitalizacionService = Depends(get_orden_hospitalizacion_service),
):
    """Crear una nueva orden de hospitalización"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Orden creada correctamente"
    )


@router.get("/{id}", response_model=OrdenHospitalizacionResponse)
async def obtener_orden(
    id: int, service: OrdenHospitalizacionService = Depends(get_orden_hospitalizacion_service)
):
    """Obtener una orden por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Orden obtenida correctamente"
    )


@router.patch("/{id}", response_model=OrdenHospitalizacionResponse)
async def actualizar_orden(
    id: int,
    data: OrdenHospitalizacionUpdate,
    service: OrdenHospitalizacionService = Depends(get_orden_hospitalizacion_service),
):
    """Actualizar una orden de hospitalización"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Orden actualizada correctamente"
    )


@router.delete("/{id}")
async def eliminar_orden(
    id: int, service: OrdenHospitalizacionService = Depends(get_orden_hospitalizacion_service)
):
    """Eliminar una orden de hospitalización"""
    await service.delete(id)
    return success_response(message="Orden eliminada correctamente")


@router.get("/paciente/{id_paciente}", response_model=list[OrdenHospitalizacionResponse])
async def listar_por_paciente(
    id_paciente: int,
    service: OrdenHospitalizacionService = Depends(get_orden_hospitalizacion_service),
):
    """Listar órdenes de un paciente"""
    items = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Órdenes del paciente listadas correctamente",
    )
