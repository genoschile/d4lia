from fastapi import APIRouter, Depends
from app.modules.receta_medicamento.schemas.receta_medicamento_schema import (
    RecetaMedicamentoResponse,
    RecetaMedicamentoCreate,
    RecetaMedicamentoUpdate,
    RecetaMedicamentoDetailed,
)
from app.modules.receta_medicamento.services.receta_medicamento_service import RecetaMedicamentoService
from app.modules.instance import get_receta_medicamento_service
from app.helpers.response import success_response

router = APIRouter(prefix="/receta_medicamento", tags=["Receta-Medicamento"])


@router.get("/", response_model=list[RecetaMedicamentoDetailed])
async def listar_prescripciones(
    service: RecetaMedicamentoService = Depends(get_receta_medicamento_service),
):
    """Listar todas las prescripciones (receta-medicamento)"""
    prescripciones = await service.list_all()
    return success_response(
        data=[p.model_dump() for p in prescripciones],
        message="Prescripciones listadas correctamente",
    )


@router.post("/", response_model=RecetaMedicamentoResponse)
async def agregar_medicamento_a_receta(
    data: RecetaMedicamentoCreate,
    service: RecetaMedicamentoService = Depends(get_receta_medicamento_service),
):
    """Agregar un medicamento a una receta con detalles de prescripción"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), 
        message="Medicamento agregado a la receta correctamente"
    )


@router.patch("/{id_receta}/{id_medicamento}", response_model=RecetaMedicamentoResponse)
async def actualizar_prescripcion(
    id_receta: int,
    id_medicamento: int,
    data: RecetaMedicamentoUpdate,
    service: RecetaMedicamentoService = Depends(get_receta_medicamento_service),
):
    """Actualizar detalles de prescripción (dosis, frecuencia, etc.)"""
    updated = await service.update(id_receta, id_medicamento, data)
    return success_response(
        data=updated.model_dump(), 
        message="Prescripción actualizada correctamente"
    )


@router.delete("/{id_receta}/{id_medicamento}")
async def eliminar_medicamento_de_receta(
    id_receta: int,
    id_medicamento: int,
    service: RecetaMedicamentoService = Depends(get_receta_medicamento_service),
):
    """Eliminar un medicamento de una receta"""
    await service.delete(id_receta, id_medicamento)
    return success_response(
        message="Medicamento eliminado de la receta correctamente"
    )


@router.get("/receta/{id_receta}/medicamentos", response_model=list[RecetaMedicamentoDetailed])
async def obtener_medicamentos_de_receta(
    id_receta: int,
    service: RecetaMedicamentoService = Depends(get_receta_medicamento_service),
):
    """Obtener todos los medicamentos de una receta con detalles de prescripción"""
    medicamentos = await service.get_medicamentos_by_receta(id_receta)
    return success_response(
        data=[m.model_dump() for m in medicamentos],
        message="Medicamentos de la receta obtenidos correctamente",
    )


@router.get("/medicamento/{id_medicamento}/recetas")
async def obtener_recetas_con_medicamento(
    id_medicamento: int,
    service: RecetaMedicamentoService = Depends(get_receta_medicamento_service),
):
    """Obtener todas las recetas que incluyen un medicamento"""
    recetas = await service.get_recetas_by_medicamento(id_medicamento)
    return success_response(
        data=recetas,
        message="Recetas con el medicamento obtenidas correctamente",
    )
