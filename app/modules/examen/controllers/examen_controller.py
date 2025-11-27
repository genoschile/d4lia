from fastapi import APIRouter, Depends
from app.modules.examen.schemas.examen_schema import (
    ExamenResponse,
    ExamenCreate,
    ExamenUpdate,
)
from app.modules.examen.services.examen_service import ExamenService
from app.modules.instance import get_examen_service
from app.helpers.response import success_response

router = APIRouter(prefix="/examen", tags=["Resultados de Examen"])


@router.get("/", response_model=list[ExamenResponse])
async def listar_examenes(
    service: ExamenService = Depends(get_examen_service),
):
    """Listar todos los resultados de examen"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Resultados listados correctamente",
    )


@router.post("/", response_model=ExamenResponse)
async def crear_examen(
    data: ExamenCreate,
    service: ExamenService = Depends(get_examen_service),
):
    """Registrar un nuevo resultado de examen"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Resultado registrado correctamente"
    )


@router.get("/{id}", response_model=ExamenResponse)
async def obtener_examen(
    id: int, service: ExamenService = Depends(get_examen_service)
):
    """Obtener un resultado por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Resultado obtenido correctamente"
    )


@router.patch("/{id}", response_model=ExamenResponse)
async def actualizar_examen(
    id: int,
    data: ExamenUpdate,
    service: ExamenService = Depends(get_examen_service),
):
    """Actualizar un resultado de examen"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Resultado actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_examen(
    id: int, service: ExamenService = Depends(get_examen_service)
):
    """Eliminar un resultado de examen"""
    await service.delete(id)
    return success_response(message="Resultado eliminado correctamente")


@router.get("/paciente/{id_paciente}", response_model=list[ExamenResponse])
async def listar_por_paciente(
    id_paciente: int,
    service: ExamenService = Depends(get_examen_service),
):
    """Listar resultados de un paciente"""
    items = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Resultados del paciente listados correctamente",
    )


@router.get("/orden/{id_orden}", response_model=list[ExamenResponse])
async def listar_por_orden(
    id_orden: int,
    service: ExamenService = Depends(get_examen_service),
):
    """Listar resultados asociados a una orden"""
    items = await service.get_by_orden(id_orden)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Resultados de la orden listados correctamente",
    )
