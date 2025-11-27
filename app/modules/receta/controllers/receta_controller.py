from fastapi import APIRouter, Depends
from app.modules.receta.schemas.receta_schema import (
    RecetaResponse,
    RecetaCreate,
    RecetaUpdate,
)
from app.modules.receta.services.receta_service import RecetaService
from app.modules.instance import get_receta_service
from app.helpers.response import success_response

router = APIRouter(prefix="/receta", tags=["Receta"])


@router.get("/", response_model=list[RecetaResponse])
async def listar_recetas(
    service: RecetaService = Depends(get_receta_service),
):
    """Listar todas las recetas"""
    recetas = await service.list_all()
    return success_response(
        data=[r.model_dump() for r in recetas],
        message="Recetas listadas correctamente",
    )


@router.post("/", response_model=RecetaResponse)
async def crear_receta(
    receta: RecetaCreate,
    service: RecetaService = Depends(get_receta_service),
):
    """Crear una nueva receta"""
    created = await service.create(receta)
    return success_response(
        data=created.model_dump(), message="Receta creada correctamente"
    )


@router.get("/{id}", response_model=RecetaResponse)
async def obtener_receta(
    id: int, service: RecetaService = Depends(get_receta_service)
):
    """Obtener una receta por ID"""
    receta = await service.get_by_id(id)
    return success_response(
        data=receta.model_dump(), message="Receta obtenida correctamente"
    )


@router.patch("/{id}", response_model=RecetaResponse)
async def actualizar_receta(
    id: int,
    receta: RecetaUpdate,
    service: RecetaService = Depends(get_receta_service),
):
    """Actualizar una receta"""
    updated = await service.update(id, receta)
    return success_response(
        data=updated.model_dump(), message="Receta actualizada correctamente"
    )


@router.delete("/{id}")
async def eliminar_receta(
    id: int, service: RecetaService = Depends(get_receta_service)
):
    """Eliminar una receta"""
    await service.delete(id)
    return success_response(message="Receta eliminada correctamente")


@router.get("/paciente/{id_paciente}", response_model=list[RecetaResponse])
async def listar_recetas_por_paciente(
    id_paciente: int,
    service: RecetaService = Depends(get_receta_service),
):
    """Listar recetas de un paciente"""
    recetas = await service.get_by_paciente(id_paciente)
    return success_response(
        data=[r.model_dump() for r in recetas],
        message="Recetas del paciente listadas correctamente",
    )


@router.get("/medico/{id_medico}", response_model=list[RecetaResponse])
async def listar_recetas_por_medico(
    id_medico: int,
    service: RecetaService = Depends(get_receta_service),
):
    """Listar recetas de un médico"""
    recetas = await service.get_by_medico(id_medico)
    return success_response(
        data=[r.model_dump() for r in recetas],
        message="Recetas del médico listadas correctamente",
    )


@router.get("/consulta/{id_consulta}", response_model=list[RecetaResponse])
async def listar_recetas_por_consulta(
    id_consulta: int,
    service: RecetaService = Depends(get_receta_service),
):
    """Listar recetas de una consulta médica"""
    recetas = await service.get_by_consulta(id_consulta)
    return success_response(
        data=[r.model_dump() for r in recetas],
        message="Recetas de la consulta listadas correctamente",
    )
