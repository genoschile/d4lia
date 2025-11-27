from fastapi import APIRouter, Depends, Query
from app.modules.ges.schemas.ges_schema import (
    GesResponse,
    GesCreate,
    GesUpdate,
)
from app.modules.ges.services.ges_service import GesService
from app.modules.instance import get_ges_service
from app.helpers.response import success_response

router = APIRouter(prefix="/ges", tags=["GES"])


@router.get("/", response_model=list[GesResponse])
async def listar_ges(
    service: GesService = Depends(get_ges_service),
):
    """Listar todos los programas GES"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Programas GES listados correctamente",
    )


@router.get("/search", response_model=list[GesResponse])
async def buscar_ges(
    q: str = Query(..., min_length=2, description="Término de búsqueda (código o nombre)"),
    service: GesService = Depends(get_ges_service),
):
    """Buscar programas GES por código o nombre"""
    items = await service.search(q)
    return success_response(
        data=[i.model_dump() for i in items],
        message=f"Resultados de búsqueda para '{q}'",
    )


@router.post("/", response_model=GesResponse)
async def crear_ges(
    data: GesCreate,
    service: GesService = Depends(get_ges_service),
):
    """Crear un nuevo programa GES"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Programa GES creado correctamente"
    )


@router.get("/{id}", response_model=GesResponse)
async def obtener_ges(
    id: int, service: GesService = Depends(get_ges_service)
):
    """Obtener un programa GES por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Programa GES obtenido correctamente"
    )


@router.patch("/{id}", response_model=GesResponse)
async def actualizar_ges(
    id: int,
    data: GesUpdate,
    service: GesService = Depends(get_ges_service),
):
    """Actualizar un programa GES"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Programa GES actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_ges(
    id: int, service: GesService = Depends(get_ges_service)
):
    """Eliminar un programa GES"""
    await service.delete(id)
    return success_response(message="Programa GES eliminado correctamente")
