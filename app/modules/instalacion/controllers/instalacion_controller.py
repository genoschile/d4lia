from fastapi import APIRouter, Depends
from app.modules.instalacion.schemas.instalacion_schema import (
    InstalacionResponse,
    InstalacionCreate,
    InstalacionUpdate,
    TipoInstalacionEnum,
)
from app.modules.instalacion.services.instalacion_service import InstalacionService
from app.modules.instance import get_instalacion_service
from app.helpers.response import success_response

router = APIRouter(prefix="/instalacion", tags=["Instalación"])


@router.get("/", response_model=list[InstalacionResponse])
async def listar_instalaciones(
    service: InstalacionService = Depends(get_instalacion_service),
):
    """Listar todas las instalaciones"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Instalaciones listadas correctamente",
    )


@router.post("/", response_model=InstalacionResponse)
async def crear_instalacion(
    data: InstalacionCreate,
    service: InstalacionService = Depends(get_instalacion_service),
):
    """Crear una nueva instalación"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="Instalación creada correctamente"
    )


@router.get("/{id}", response_model=InstalacionResponse)
async def obtener_instalacion(
    id: int, service: InstalacionService = Depends(get_instalacion_service)
):
    """Obtener una instalación por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Instalación obtenida correctamente"
    )


@router.patch("/{id}", response_model=InstalacionResponse)
async def actualizar_instalacion(
    id: int,
    data: InstalacionUpdate,
    service: InstalacionService = Depends(get_instalacion_service),
):
    """Actualizar una instalación"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Instalación actualizada correctamente"
    )


@router.delete("/{id}")
async def eliminar_instalacion(
    id: int, service: InstalacionService = Depends(get_instalacion_service)
):
    """Eliminar una instalación"""
    await service.delete(id)
    return success_response(message="Instalación eliminada correctamente")


@router.get("/tipo/{tipo}", response_model=list[InstalacionResponse])
async def listar_por_tipo(
    tipo: TipoInstalacionEnum,
    service: InstalacionService = Depends(get_instalacion_service),
):
    """Listar instalaciones por tipo"""
    items = await service.get_by_tipo(tipo)
    return success_response(
        data=[i.model_dump() for i in items],
        message=f"Instalaciones de tipo '{tipo.value}' listadas correctamente",
    )
