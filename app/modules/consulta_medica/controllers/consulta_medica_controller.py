from fastapi import APIRouter, Depends, Query
from datetime import date
from app.modules.consulta_medica.schemas.consulta_medica_schema import (
    ConsultaMedicaResponse,
    ConsultaMedicaCreate,
    ConsultaMedicaUpdate,
)
from app.modules.consulta_medica.services.consulta_medica_service import (
    ConsultaMedicaService,
)
from app.modules.instance import get_consulta_medica_service
from app.helpers.response import success_response

router = APIRouter(prefix="/consulta_medica", tags=["Consulta Médica"])


@router.get("/", response_model=list[ConsultaMedicaResponse])
async def listar_consultas(
    service: ConsultaMedicaService = Depends(get_consulta_medica_service),
):
    consultas = await service.list_all()
    return success_response(
        data=[c.model_dump() for c in consultas],
        message="Consultas médicas listadas correctamente",
    )


@router.post("/", response_model=ConsultaMedicaResponse)
async def crear_consulta(
    consulta: ConsultaMedicaCreate,
    service: ConsultaMedicaService = Depends(get_consulta_medica_service),
):
    created = await service.create(consulta)
    return success_response(
        data=created.model_dump(), message="Consulta médica creada correctamente"
    )


@router.get("/{id}", response_model=ConsultaMedicaResponse)
async def obtener_consulta(
    id: int, service: ConsultaMedicaService = Depends(get_consulta_medica_service)
):
    consulta = await service.get_by_id(id)
    return success_response(
        data=consulta.model_dump(), message="Consulta médica obtenida correctamente"
    )


@router.patch("/{id}", response_model=ConsultaMedicaResponse)
async def actualizar_consulta(
    id: int,
    consulta: ConsultaMedicaUpdate,
    service: ConsultaMedicaService = Depends(get_consulta_medica_service),
):
    updated = await service.update(id, consulta)
    return success_response(
        data=updated.model_dump(), message="Consulta médica actualizada correctamente"
    )


@router.delete("/{id}")
async def eliminar_consulta(
    id: int, service: ConsultaMedicaService = Depends(get_consulta_medica_service)
):
    await service.delete(id)
    return success_response(message="Consulta médica eliminada correctamente")


@router.get("/paciente/{id_paciente}", response_model=list[ConsultaMedicaResponse])
async def listar_consultas_por_paciente(
    id_paciente: int,
    service: ConsultaMedicaService = Depends(get_consulta_medica_service),
):
    consultas = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[c.model_dump() for c in consultas],
        message="Consultas del paciente listadas correctamente",
    )


@router.get("/profesional/{id_profesional}", response_model=list[ConsultaMedicaResponse])
async def listar_consultas_por_profesional(
    id_profesional: int,
    service: ConsultaMedicaService = Depends(get_consulta_medica_service),
):
    consultas = await service.get_by_profesional(id_profesional)
    return success_response(
        data=[c.model_dump() for c in consultas],
        message="Consultas del profesional listadas correctamente",
    )


@router.get("/fecha/rango", response_model=list[ConsultaMedicaResponse])
async def listar_consultas_por_fecha(
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    service: ConsultaMedicaService = Depends(get_consulta_medica_service),
):
    consultas = await service.get_by_fecha_range(fecha_inicio, fecha_fin)
    return success_response(
        data=[c.model_dump() for c in consultas],
        message="Consultas en el rango de fechas listadas correctamente",
    )
