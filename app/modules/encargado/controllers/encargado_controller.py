from fastapi import APIRouter, Depends
from app.modules.encargado.schemas.encargado_schema import (
    EncargadoResponse,
    EncargadoCreate,
    EncargadoUpdate,
    CargoEnum,
)
from app.modules.encargado.services.encargado_service import EncargadoService
from app.modules.instance import get_encargado_service
from app.helpers.response import success_response

router = APIRouter(prefix="/encargado", tags=["Encargado"])


@router.get("/", response_model=list[EncargadoResponse])
async def listar_encargados(
    service: EncargadoService = Depends(get_encargado_service),
):
    """Listar todos los encargados (personal)"""
    encargados = await service.list_all()
    return success_response(
        data=[e.model_dump() for e in encargados],
        message="Encargados listados correctamente",
    )


@router.post("/", response_model=EncargadoResponse)
async def crear_encargado(
    encargado: EncargadoCreate,
    service: EncargadoService = Depends(get_encargado_service),
):
    """Crear un nuevo encargado"""
    created = await service.create(encargado)
    return success_response(
        data=created.model_dump(), message="Encargado creado correctamente"
    )


@router.get("/{id}", response_model=EncargadoResponse)
async def obtener_encargado(
    id: int, service: EncargadoService = Depends(get_encargado_service)
):
    """Obtener un encargado por ID"""
    encargado = await service.get_by_id(id)
    return success_response(
        data=encargado.model_dump(), message="Encargado obtenido correctamente"
    )


@router.patch("/{id}", response_model=EncargadoResponse)
async def actualizar_encargado(
    id: int,
    encargado: EncargadoUpdate,
    service: EncargadoService = Depends(get_encargado_service),
):
    """Actualizar un encargado"""
    updated = await service.update(id, encargado)
    return success_response(
        data=updated.model_dump(), message="Encargado actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_encargado(
    id: int, service: EncargadoService = Depends(get_encargado_service)
):
    """Eliminar un encargado"""
    await service.delete(id)
    return success_response(message="Encargado eliminado correctamente")


@router.get("/cargo/{cargo}", response_model=list[EncargadoResponse])
async def listar_por_cargo(
    cargo: CargoEnum,
    service: EncargadoService = Depends(get_encargado_service),
):
    """Listar encargados por cargo (enfermero, doctor, técnico, administrativo, otro)"""
    encargados = await service.get_by_cargo(cargo.value)
    return success_response(
        data=[e.model_dump() for e in encargados],
        message=f"Encargados con cargo '{cargo.value}' listados correctamente",
    )


@router.get("/activos/lista", response_model=list[EncargadoResponse])
async def listar_activos(
    service: EncargadoService = Depends(get_encargado_service),
):
    """Listar encargados activos"""
    encargados = await service.get_activos()
    return success_response(
        data=[e.model_dump() for e in encargados],
        message="Encargados activos listados correctamente",
    )
