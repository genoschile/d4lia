from fastapi import APIRouter, Depends, Query
from app.modules.medicamento.schemas.medicamento_schema import (
    MedicamentoResponse,
    MedicamentoCreate,
    MedicamentoUpdate,
)
from app.modules.medicamento.services.medicamento_service import MedicamentoService
from app.modules.instance import get_medicamento_service
from app.helpers.response import success_response

router = APIRouter(prefix="/medicamento", tags=["Medicamento"])


@router.get("/", response_model=list[MedicamentoResponse])
async def listar_medicamentos(
    service: MedicamentoService = Depends(get_medicamento_service),
):
    """Listar todos los medicamentos"""
    medicamentos = await service.list_all()
    return success_response(
        data=[m.model_dump() for m in medicamentos],
        message="Medicamentos listados correctamente",
    )


@router.post("/", response_model=MedicamentoResponse)
async def crear_medicamento(
    medicamento: MedicamentoCreate,
    service: MedicamentoService = Depends(get_medicamento_service),
):
    """Crear un nuevo medicamento"""
    created = await service.create(medicamento)
    return success_response(
        data=created.model_dump(), message="Medicamento creado correctamente"
    )


@router.get("/{id}", response_model=MedicamentoResponse)
async def obtener_medicamento(
    id: int, service: MedicamentoService = Depends(get_medicamento_service)
):
    """Obtener un medicamento por ID"""
    medicamento = await service.get_by_id(id)
    return success_response(
        data=medicamento.model_dump(), message="Medicamento obtenido correctamente"
    )


@router.patch("/{id}", response_model=MedicamentoResponse)
async def actualizar_medicamento(
    id: int,
    medicamento: MedicamentoUpdate,
    service: MedicamentoService = Depends(get_medicamento_service),
):
    """Actualizar un medicamento"""
    updated = await service.update(id, medicamento)
    return success_response(
        data=updated.model_dump(), message="Medicamento actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_medicamento(
    id: int, service: MedicamentoService = Depends(get_medicamento_service)
):
    """Eliminar un medicamento"""
    await service.delete(id)
    return success_response(message="Medicamento eliminado correctamente")


@router.get("/stock/bajo", response_model=list[MedicamentoResponse])
async def listar_stock_bajo(
    umbral: int = Query(default=10, ge=1, description="Umbral de stock bajo"),
    service: MedicamentoService = Depends(get_medicamento_service),
):
    """Listar medicamentos con stock bajo"""
    medicamentos = await service.get_stock_bajo(umbral)
    return success_response(
        data=[m.model_dump() for m in medicamentos],
        message=f"Medicamentos con stock bajo (≤{umbral}) listados correctamente",
    )


@router.get("/laboratorio/{laboratorio}", response_model=list[MedicamentoResponse])
async def listar_por_laboratorio(
    laboratorio: str,
    service: MedicamentoService = Depends(get_medicamento_service),
):
    """Listar medicamentos por laboratorio"""
    medicamentos = await service.get_by_laboratorio(laboratorio)
    return success_response(
        data=[m.model_dump() for m in medicamentos],
        message=f"Medicamentos del laboratorio '{laboratorio}' listados correctamente",
    )
