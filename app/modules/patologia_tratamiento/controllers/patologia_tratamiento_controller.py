from fastapi import APIRouter, Depends
from app.modules.patologia_tratamiento.schemas.patologia_tratamiento_schema import (
    PatologiaTratamientoResponse,
    PatologiaTratamientoCreate,
    PatologiaTratamientoDetailed,
)
from app.modules.patologia_tratamiento.services.patologia_tratamiento_service import PatologiaTratamientoService
from app.modules.instance import get_patologia_tratamiento_service
from app.helpers.response import success_response

router = APIRouter(prefix="/patologia_tratamiento", tags=["Patología-Tratamiento"])


@router.get("/", response_model=list[PatologiaTratamientoDetailed])
async def listar_relaciones(
    service: PatologiaTratamientoService = Depends(get_patologia_tratamiento_service),
):
    """Listar todas las relaciones patología-tratamiento"""
    relaciones = await service.list_all()
    return success_response(
        data=[r.model_dump() for r in relaciones],
        message="Relaciones listadas correctamente",
    )


@router.post("/", response_model=PatologiaTratamientoResponse)
async def vincular_patologia_tratamiento(
    data: PatologiaTratamientoCreate,
    service: PatologiaTratamientoService = Depends(get_patologia_tratamiento_service),
):
    """Vincular una patología con un tratamiento"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), 
        message="Patología y tratamiento vinculados correctamente"
    )


@router.delete("/{id_patologia}/{id_tratamiento}")
async def desvincular_patologia_tratamiento(
    id_patologia: int,
    id_tratamiento: int,
    service: PatologiaTratamientoService = Depends(get_patologia_tratamiento_service),
):
    """Desvincular una patología de un tratamiento"""
    await service.delete(id_patologia, id_tratamiento)
    return success_response(
        message="Patología y tratamiento desvinculados correctamente"
    )


@router.get("/patologia/{id_patologia}/tratamientos")
async def obtener_tratamientos_por_patologia(
    id_patologia: int,
    service: PatologiaTratamientoService = Depends(get_patologia_tratamiento_service),
):
    """Obtener todos los tratamientos de una patología"""
    tratamientos = await service.get_tratamientos_by_patologia(id_patologia)
    return success_response(
        data=tratamientos,
        message="Tratamientos obtenidos correctamente",
    )


@router.get("/tratamiento/{id_tratamiento}/patologias")
async def obtener_patologias_por_tratamiento(
    id_tratamiento: int,
    service: PatologiaTratamientoService = Depends(get_patologia_tratamiento_service),
):
    """Obtener todas las patologías asociadas a un tratamiento"""
    patologias = await service.get_patologias_by_tratamiento(id_tratamiento)
    return success_response(
        data=patologias,
        message="Patologías obtenidas correctamente",
    )
