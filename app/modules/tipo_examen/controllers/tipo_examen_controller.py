from fastapi import APIRouter, Depends
from app.modules.tipo_examen.schemas.tipo_examen_schema import (
    TipoExamenResponse,
    TipoExamenCreate,
    TipoExamenUpdate,
)
from app.modules.tipo_examen.services.tipo_examen_service import TipoExamenService
from app.modules.instance import get_tipo_examen_service
from app.helpers.response import success_response

router = APIRouter(prefix="/tipo_examen", tags=["Tipo Examen"])


@router.get("/", response_model=list[TipoExamenResponse])
async def listar_tipos_examen(
    service: TipoExamenService = Depends(get_tipo_examen_service),
):
    """Listar todos los tipos de examen"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Tipos de examen listados correctamente",
    )


@router.post("/", response_model=TipoExamenResponse)
async def crear_tipo_examen(
    data: TipoExamenCreate,
    service: TipoExamenService = Depends(get_tipo_examen_service),
):
    """Crear un nuevo tipo de examen"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Tipo de examen creado correctamente"
    )


@router.get("/{id}", response_model=TipoExamenResponse)
async def obtener_tipo_examen(
    id: int, service: TipoExamenService = Depends(get_tipo_examen_service)
):
    """Obtener un tipo de examen por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Tipo de examen obtenido correctamente"
    )


@router.patch("/{id}", response_model=TipoExamenResponse)
async def actualizar_tipo_examen(
    id: int,
    data: TipoExamenUpdate,
    service: TipoExamenService = Depends(get_tipo_examen_service),
):
    """Actualizar un tipo de examen"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Tipo de examen actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_tipo_examen(
    id: int, service: TipoExamenService = Depends(get_tipo_examen_service)
):
    """Eliminar un tipo de examen"""
    await service.delete(id)
    return success_response(message="Tipo de examen eliminado correctamente")
