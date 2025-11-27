from fastapi import APIRouter, Depends
from app.modules.hospitalizacion.schemas.hospitalizacion_schema import (
    HospitalizacionResponse,
    HospitalizacionCreate,
    HospitalizacionUpdate,
)
from app.modules.hospitalizacion.services.hospitalizacion_service import HospitalizacionService
from app.modules.instance import get_hospitalizacion_service
from app.helpers.response import success_response

router = APIRouter(prefix="/hospitalizacion", tags=["Hospitalización"])


@router.get("/", response_model=list[HospitalizacionResponse])
async def listar_hospitalizaciones(
    service: HospitalizacionService = Depends(get_hospitalizacion_service),
):
    """Listar todas las hospitalizaciones"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Hospitalizaciones listadas correctamente",
    )


@router.post("/", response_model=HospitalizacionResponse)
async def crear_hospitalizacion(
    data: HospitalizacionCreate,
    service: HospitalizacionService = Depends(get_hospitalizacion_service),
):
    """Registrar un nuevo ingreso de hospitalización"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Hospitalización registrada correctamente"
    )


@router.get("/{id}", response_model=HospitalizacionResponse)
async def obtener_hospitalizacion(
    id: int, service: HospitalizacionService = Depends(get_hospitalizacion_service)
):
    """Obtener una hospitalización por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Hospitalización obtenida correctamente"
    )


@router.patch("/{id}", response_model=HospitalizacionResponse)
async def actualizar_hospitalizacion(
    id: int,
    data: HospitalizacionUpdate,
    service: HospitalizacionService = Depends(get_hospitalizacion_service),
):
    """Actualizar una hospitalización"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Hospitalización actualizada correctamente"
    )


@router.delete("/{id}")
async def eliminar_hospitalizacion(
    id: int, service: HospitalizacionService = Depends(get_hospitalizacion_service)
):
    """Eliminar una hospitalización"""
    await service.delete(id)
    return success_response(message="Hospitalización eliminada correctamente")


@router.get("/paciente/{id_paciente}", response_model=list[HospitalizacionResponse])
async def listar_por_paciente(
    id_paciente: int,
    service: HospitalizacionService = Depends(get_hospitalizacion_service),
):
    """Listar hospitalizaciones de un paciente"""
    items = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Hospitalizaciones del paciente listadas correctamente",
    )


@router.get("/estado/activas", response_model=list[HospitalizacionResponse])
async def listar_activas(
    service: HospitalizacionService = Depends(get_hospitalizacion_service),
):
    """Listar hospitalizaciones activas"""
    items = await service.get_activas()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Hospitalizaciones activas listadas correctamente",
    )
