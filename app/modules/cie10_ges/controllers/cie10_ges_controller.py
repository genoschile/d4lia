from fastapi import APIRouter, Depends
from app.modules.cie10_ges.schemas.cie10_ges_schema import (
    Cie10GesResponse,
    Cie10GesCreate,
    Cie10GesDetailed,
)
from app.modules.cie10_ges.services.cie10_ges_service import Cie10GesService
from app.modules.instance import get_cie10_ges_service
from app.helpers.response import success_response

router = APIRouter(prefix="/cie10_ges", tags=["CIE10-GES"])


@router.get("/", response_model=list[Cie10GesDetailed])
async def listar_relaciones(
    service: Cie10GesService = Depends(get_cie10_ges_service),
):
    """Listar todas las relaciones CIE10-GES"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Relaciones listadas correctamente",
    )


@router.post("/", response_model=Cie10GesResponse)
async def crear_relacion(
    data: Cie10GesCreate,
    service: Cie10GesService = Depends(get_cie10_ges_service),
):
    """Vincular un código CIE-10 con un programa GES"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), 
        message="Relación creada correctamente"
    )


@router.delete("/{id_cie10}/{id_ges}")
async def eliminar_relacion(
    id_cie10: int,
    id_ges: int,
    service: Cie10GesService = Depends(get_cie10_ges_service),
):
    """Eliminar vínculo entre CIE-10 y GES"""
    await service.delete(id_cie10, id_ges)
    return success_response(
        message="Relación eliminada correctamente"
    )


@router.get("/cie10/{id_cie10}/ges", response_model=list[Cie10GesDetailed])
async def obtener_ges_de_cie10(
    id_cie10: int,
    service: Cie10GesService = Depends(get_cie10_ges_service),
):
    """Obtener programas GES asociados a un código CIE-10"""
    items = await service.get_ges_by_cie10(id_cie10)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Programas GES obtenidos correctamente",
    )


@router.get("/ges/{id_ges}/cie10", response_model=list[Cie10GesDetailed])
async def obtener_cie10_de_ges(
    id_ges: int,
    service: Cie10GesService = Depends(get_cie10_ges_service),
):
    """Obtener códigos CIE-10 asociados a un programa GES"""
    items = await service.get_cie10_by_ges(id_ges)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Códigos CIE-10 obtenidos correctamente",
    )
