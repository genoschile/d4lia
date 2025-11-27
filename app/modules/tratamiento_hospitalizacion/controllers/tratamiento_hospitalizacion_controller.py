from fastapi import APIRouter, Depends
from app.modules.tratamiento_hospitalizacion.schemas.tratamiento_hospitalizacion_schema import (
    TratamientoHospitalizacionResponse,
    TratamientoHospitalizacionCreate,
    TratamientoHospitalizacionDetailed,
)
from app.modules.tratamiento_hospitalizacion.services.tratamiento_hospitalizacion_service import TratamientoHospitalizacionService
from app.modules.instance import get_tratamiento_hospitalizacion_service
from app.helpers.response import success_response

router = APIRouter(prefix="/tratamiento_hospitalizacion", tags=["Tratamiento Hospitalización"])


@router.get("/", response_model=list[TratamientoHospitalizacionResponse])
async def listar_tratamientos_hospitalizacion(
    service: TratamientoHospitalizacionService = Depends(get_tratamiento_hospitalizacion_service),
):
    """Listar todos los tratamientos en hospitalizaciones"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Registros listados correctamente",
    )


@router.post("/", response_model=TratamientoHospitalizacionResponse)
async def asignar_tratamiento(
    data: TratamientoHospitalizacionCreate,
    service: TratamientoHospitalizacionService = Depends(get_tratamiento_hospitalizacion_service),
):
    """Asignar un tratamiento a una hospitalización"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Tratamiento asignado correctamente"
    )


@router.delete("/{id_hospitalizacion}/{id_tratamiento}")
async def eliminar_asignacion(
    id_hospitalizacion: int,
    id_tratamiento: int,
    service: TratamientoHospitalizacionService = Depends(get_tratamiento_hospitalizacion_service),
):
    """Eliminar un tratamiento de una hospitalización"""
    await service.delete(id_hospitalizacion, id_tratamiento)
    return success_response(message="Asignación eliminada correctamente")


@router.get("/hospitalizacion/{id}", response_model=list[TratamientoHospitalizacionDetailed])
async def listar_por_hospitalizacion(
    id: int,
    service: TratamientoHospitalizacionService = Depends(get_tratamiento_hospitalizacion_service),
):
    """Listar tratamientos de una hospitalización específica"""
    items = await service.get_by_hospitalizacion(id)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Tratamientos de la hospitalización listados correctamente",
    )
