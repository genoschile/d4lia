from fastapi import APIRouter, Depends
from app.modules.medicamento_hospitalizacion.schemas.medicamento_hospitalizacion_schema import (
    MedicamentoHospitalizacionResponse,
    MedicamentoHospitalizacionCreate,
    MedicamentoHospitalizacionDetailed,
)
from app.modules.medicamento_hospitalizacion.services.medicamento_hospitalizacion_service import MedicamentoHospitalizacionService
from app.modules.instance import get_medicamento_hospitalizacion_service
from app.helpers.response import success_response

router = APIRouter(prefix="/medicamento_hospitalizacion", tags=["Medicamento Hospitalización"])


@router.get("/", response_model=list[MedicamentoHospitalizacionResponse])
async def listar_medicamentos_hospitalizacion(
    service: MedicamentoHospitalizacionService = Depends(get_medicamento_hospitalizacion_service),
):
    """Listar todos los medicamentos en hospitalizaciones"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Registros listados correctamente",
    )


@router.post("/", response_model=MedicamentoHospitalizacionResponse)
async def asignar_medicamento(
    data: MedicamentoHospitalizacionCreate,
    service: MedicamentoHospitalizacionService = Depends(get_medicamento_hospitalizacion_service),
):
    """Asignar un medicamento a una hospitalización"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Medicamento asignado correctamente"
    )


@router.delete("/{id_hospitalizacion}/{id_medicamento}")
async def eliminar_asignacion(
    id_hospitalizacion: int,
    id_medicamento: int,
    service: MedicamentoHospitalizacionService = Depends(get_medicamento_hospitalizacion_service),
):
    """Eliminar un medicamento de una hospitalización"""
    await service.delete(id_hospitalizacion, id_medicamento)
    return success_response(message="Asignación eliminada correctamente")


@router.get("/hospitalizacion/{id}", response_model=list[MedicamentoHospitalizacionDetailed])
async def listar_por_hospitalizacion(
    id: int,
    service: MedicamentoHospitalizacionService = Depends(get_medicamento_hospitalizacion_service),
):
    """Listar medicamentos de una hospitalización específica"""
    items = await service.get_by_hospitalizacion(id)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Medicamentos de la hospitalización listados correctamente",
    )
