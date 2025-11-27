from fastapi import APIRouter, Depends
from app.modules.diagnostico.schemas.diagnostico_schema import (
    DiagnosticoResponse,
    DiagnosticoCreate,
    DiagnosticoUpdate,
    TipoDiagnosticoEnum,
)
from app.modules.diagnostico.services.diagnostico_service import DiagnosticoService
from app.modules.instance import get_diagnostico_service
from app.helpers.response import success_response

router = APIRouter(prefix="/diagnostico", tags=["Diagnóstico"])


@router.get("/", response_model=list[DiagnosticoResponse])
async def listar_diagnosticos(
    service: DiagnosticoService = Depends(get_diagnostico_service),
):
    """Listar todos los diagnósticos"""
    diagnosticos = await service.list_all()
    return success_response(
        data=[d.model_dump() for d in diagnosticos],
        message="Diagnósticos listados correctamente",
    )


@router.post("/", response_model=DiagnosticoResponse)
async def crear_diagnostico(
    diagnostico: DiagnosticoCreate,
    service: DiagnosticoService = Depends(get_diagnostico_service),
):
    """Crear un nuevo diagnóstico"""
    created = await service.create(diagnostico)
    return success_response(
        data=created.model_dump(), message="Diagnóstico creado correctamente"
    )


@router.get("/{id}", response_model=DiagnosticoResponse)
async def obtener_diagnostico(
    id: int, service: DiagnosticoService = Depends(get_diagnostico_service)
):
    """Obtener un diagnóstico por ID"""
    diagnostico = await service.get_by_id(id)
    return success_response(
        data=diagnostico.model_dump(), message="Diagnóstico obtenido correctamente"
    )


@router.patch("/{id}", response_model=DiagnosticoResponse)
async def actualizar_diagnostico(
    id: int,
    diagnostico: DiagnosticoUpdate,
    service: DiagnosticoService = Depends(get_diagnostico_service),
):
    """Actualizar un diagnóstico"""
    updated = await service.update(id, diagnostico)
    return success_response(
        data=updated.model_dump(), message="Diagnóstico actualizado correctamente"
    )


@router.delete("/{id}")
async def eliminar_diagnostico(
    id: int, service: DiagnosticoService = Depends(get_diagnostico_service)
):
    """Eliminar un diagnóstico"""
    await service.delete(id)
    return success_response(message="Diagnóstico eliminado correctamente")


@router.get("/consulta/{id_consulta}", response_model=list[DiagnosticoResponse])
async def listar_por_consulta(
    id_consulta: int,
    service: DiagnosticoService = Depends(get_diagnostico_service),
):
    """Listar diagnósticos de una consulta médica"""
    diagnosticos = await service.get_by_consulta(id_consulta)
    return success_response(
        data=[d.model_dump() for d in diagnosticos],
        message="Diagnósticos de la consulta listados correctamente",
    )


@router.get("/tipo/{tipo}", response_model=list[DiagnosticoResponse])
async def listar_por_tipo(
    tipo: TipoDiagnosticoEnum,
    service: DiagnosticoService = Depends(get_diagnostico_service),
):
    """Listar diagnósticos por tipo (presuntivo, confirmado, seguimiento)"""
    diagnosticos = await service.get_by_tipo(tipo)
    return success_response(
        data=[d.model_dump() for d in diagnosticos],
        message=f"Diagnósticos de tipo '{tipo.value}' listados correctamente",
    )


@router.get("/cobertura/ges", response_model=list[DiagnosticoResponse])
async def listar_con_ges(
    service: DiagnosticoService = Depends(get_diagnostico_service),
):
    """Listar diagnósticos con cobertura GES"""
    diagnosticos = await service.get_con_ges()
    return success_response(
        data=[d.model_dump() for d in diagnosticos],
        message="Diagnósticos con cobertura GES listados correctamente",
    )
