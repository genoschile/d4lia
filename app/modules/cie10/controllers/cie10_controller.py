from fastapi import APIRouter, Depends, Query
from app.modules.cie10.schemas.cie10_schema import (
    Cie10Response,
    Cie10Create,
    Cie10Update,
)
from app.modules.cie10.services.cie10_service import Cie10Service
from app.modules.instance import get_cie10_service
from app.helpers.response import success_response

router = APIRouter(prefix="/cie10", tags=["CIE-10"])


@router.get("/", response_model=list[Cie10Response])
async def listar_cie10(
    service: Cie10Service = Depends(get_cie10_service),
):
    """Listar todos los códigos CIE-10"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Códigos CIE-10 listados correctamente",
    )


@router.get("/search", response_model=list[Cie10Response])
async def buscar_cie10(
    q: str = Query(..., min_length=2, description="Término de búsqueda (código o nombre)"),
    service: Cie10Service = Depends(get_cie10_service),
):
    """Buscar códigos CIE-10 por código o nombre"""
    items = await service.search(q)
    return success_response(
        data=[i.model_dump() for i in items],
        message=f"Resultados de búsqueda para '{q}'",
    )


@router.post("/", response_model=Cie10Response)
async def crear_cie10(
    data: Cie10Create,
    service: Cie10Service = Depends(get_cie10_service),
):
    """Crear un nuevo código CIE-10"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Código CIE-10 creado correctamente"
    )


@router.get("/{id}", response_model=Cie10Response)
async def obtener_cie10(
    id: int, service: Cie10Service = Depends(get_cie10_service)
):
    """Obtener un código CIE-10 por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Código CIE-10 obtenido correctamente"
    )


@router.patch("/{id}", response_model=Cie10Response)
async def actualizar_cie10(
    id: int,
    data: Cie10Update,
    service: Cie10Service = Depends(get_cie10_service),
):
    """Actualizar un código CIE-10"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Código CIE-10 actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_cie10(
    id: int, service: Cie10Service = Depends(get_cie10_service)
):
    """Eliminar un código CIE-10"""
    await service.delete(id)
    return success_response(message="Código CIE-10 eliminado correctamente")
