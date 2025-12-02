from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.modules.paciente_ges.schemas.paciente_ges_schema import (
    PacienteGesResponse,
    PacienteGesCreate,
    PacienteGesUpdate,
    PacienteGesCountdownResponse,
    PacienteGesEstadisticas
)
from app.modules.paciente_ges.services.paciente_ges_service import PacienteGesService
from app.modules.instance import get_paciente_ges_service
from app.helpers.response import success_response

router = APIRouter(prefix="/paciente-ges", tags=["Paciente GES (Cuenta Regresiva)"])


@router.get("/", response_model=List[PacienteGesResponse])
async def listar_todos(
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """Listar todos los registros GES de pacientes"""
    items = await service.list_all()
    return success_response(
        data=[i.model_dump() for i in items],
        message="Registros listados correctamente",
    )


@router.get("/countdown", response_model=List[PacienteGesCountdownResponse])
async def ver_countdown(
    prioridad: Optional[str] = Query(None, description="Filtrar por prioridad: Crítico, Urgente, Normal, Vencido"),
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """
    Ver vista de cuenta regresiva de pacientes GES.
    Permite filtrar por prioridad (Crítico, Urgente, Normal, Vencido).
    """
    items = await service.get_countdown_view(prioridad)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Vista de cuenta regresiva obtenida correctamente",
    )


@router.get("/estadisticas", response_model=PacienteGesEstadisticas)
async def ver_estadisticas(
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """Obtener estadísticas generales de GES"""
    stats = await service.get_estadisticas()
    return success_response(
        data=stats.model_dump(),
        message="Estadísticas obtenidas correctamente",
    )


@router.post("/", response_model=PacienteGesResponse)
async def crear_paciente_ges(
    data: PacienteGesCreate,
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """Activar un nuevo GES para un paciente"""
    created = await service.create(data)
    return success_response(
        data=created.model_dump(), message="GES activado correctamente para el paciente"
    )


@router.get("/{id}", response_model=PacienteGesResponse)
async def obtener_por_id(
    id: int, service: PacienteGesService = Depends(get_paciente_ges_service)
):
    """Obtener un registro GES por ID"""
    item = await service.get_by_id(id)
    return success_response(
        data=item.model_dump(), message="Registro obtenido correctamente"
    )


@router.patch("/{id}", response_model=PacienteGesResponse)
async def actualizar_paciente_ges(
    id: int,
    data: PacienteGesUpdate,
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """Actualizar un registro GES (estado, observaciones, etc.)"""
    updated = await service.update(id, data)
    return success_response(
        data=updated.model_dump(), message="Registro actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_paciente_ges(
    id: int, service: PacienteGesService = Depends(get_paciente_ges_service)
):
    """Eliminar un registro GES"""
    await service.delete(id)
    return success_response(message="Registro eliminado correctamente")


@router.get("/paciente/{id_paciente}", response_model=List[PacienteGesResponse])
async def listar_por_paciente(
    id_paciente: int,
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """Listar todo el historial GES de un paciente"""
    items = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[i.model_dump() for i in items],
        message="Historial GES del paciente listado correctamente",
    )


@router.get("/paciente/{id_paciente}/activos", response_model=List[PacienteGesResponse])
async def listar_activos_por_paciente(
    id_paciente: int,
    service: PacienteGesService = Depends(get_paciente_ges_service),
):
    """Listar solo los GES activos de un paciente"""
    items = await service.get_activos_by_paciente(id_paciente)
    return success_response(
        data=[i.model_dump() for i in items],
        message="GES activos del paciente listados correctamente",
    )
