from fastapi import APIRouter, Depends
from app.modules.tratamiento.schemas.tratamiento_schema import (
    TratamientoResponse,
    TratamientoCreate,
    TratamientoUpdate,
)
from app.modules.tratamiento.services.tratamiento_service import TratamientoService
from app.modules.instance import get_tratamiento_service
from app.helpers.response import success_response

router = APIRouter(prefix="/tratamiento", tags=["Tratamiento"])


@router.get("/", response_model=list[TratamientoResponse])
async def listar_tratamientos(
    service: TratamientoService = Depends(get_tratamiento_service),
):
    tratamientos = await service.list_all()
    return success_response(
        data=[t.model_dump() for t in tratamientos],
        message="Tratamientos listados correctamente",
    )


@router.post("/", response_model=TratamientoResponse)
async def crear_tratamiento(
    tratamiento: TratamientoCreate,
    service: TratamientoService = Depends(get_tratamiento_service),
):
    created = await service.create(tratamiento)
    return success_response(
        data=created.model_dump(), message="Tratamiento creado correctamente"
    )


@router.get("/{id}", response_model=TratamientoResponse)
async def obtener_tratamiento(
    id: int, service: TratamientoService = Depends(get_tratamiento_service)
):
    tratamiento = await service.get_by_id(id)
    return success_response(
        data=tratamiento.model_dump(), message="Tratamiento obtenido correctamente"
    )


@router.patch("/{id}", response_model=TratamientoResponse)
async def actualizar_tratamiento(
    id: int,
    tratamiento: TratamientoUpdate,
    service: TratamientoService = Depends(get_tratamiento_service),
):
    updated = await service.update(id, tratamiento)
    return success_response(
        data=updated.model_dump(), message="Tratamiento actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_tratamiento(
    id: int, service: TratamientoService = Depends(get_tratamiento_service)
):
    await service.delete(id)
    return success_response(message="Tratamiento eliminado correctamente")
