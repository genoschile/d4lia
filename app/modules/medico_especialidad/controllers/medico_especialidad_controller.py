from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.instance import get_medico_services
from app.helpers.response import error_response, success_response
from app.modules.medico_especialidad.schemas.medico_especialidad_schema import (
    MedicoResponse,
    MedicoCreate,
    EspecialidadDTO,
    EspecialidadCreate,
    EspecialidadUpdate,
)
from app.modules.medico_especialidad.services.medico_service import MedicoService

router = APIRouter(prefix="/medico_especialidad", tags=["Médico y Especialidad"])

# ----------- MEDICOS -----------
@router.post("/medicos/", response_model=MedicoResponse)
async def crear_medico(
    medico: MedicoCreate,
    service: MedicoService = Depends(get_medico_services)
):
    created = await service.create_medico(medico)
    return success_response(
        data=created.model_dump(),
        message="Médico creado correctamente"
    )


@router.get("/medicos", response_model=list[MedicoResponse])
async def listar_medicos(service: MedicoService = Depends(get_medico_services)):
    medicos = await service.listar_medicos()
    return success_response(
        data=[m.model_dump() for m in medicos],
        message="Médicos listados correctamente"
    )


@router.get("/medicos/{medico_id}", response_model=MedicoResponse)
async def obtener_medico(medico_id: int, service: MedicoService = Depends(get_medico_services)):
    medico = await service.get_medico_by_id(medico_id)
    return success_response(
        data=medico.model_dump(),
        message="Médico obtenido correctamente"
    )


@router.get("/medicos/activos/", response_model=list[MedicoResponse])
async def listar_medicos_activos(service: MedicoService = Depends(get_medico_services)):
    medicos = await service.list_active_medicos()
    return success_response(
        data=[m.model_dump() for m in medicos],
        message="Médicos activos listados correctamente"
    )


@router.post("/medicos/{medico_id}/especialidad/{especialidad_id}")
async def asignar_especialidad(
    medico_id: int, 
    especialidad_id: int,
    service: MedicoService = Depends(get_medico_services)
):
    await service.assign_specialty(medico_id, especialidad_id)
    return success_response(
        data=None,
        message="Especialidad asignada correctamente"
    )


@router.get("/medicos/buscar/", response_model=list[MedicoResponse])
async def buscar_medicos(
    especialidad: str,
    service: MedicoService = Depends(get_medico_services)
):
    medicos = await service.search_medicos_by_specialty(especialidad)
    return success_response(
        data=[m.model_dump() for m in medicos],
        message="Médicos encontrados correctamente"
    )


# ----------- ESPECIALIDADES -----------

@router.get("/especialidades", response_model=list[EspecialidadDTO])
async def listar_especialidades(service: MedicoService = Depends(get_medico_services)):
    especialidades = await service.list_specialties()
    return success_response(
        data=[e.model_dump() for e in especialidades],
        message="Especialidades listadas correctamente"
    )

@router.post("/especialidades", response_model=EspecialidadDTO)
async def crear_especializacion(
    especializacion: EspecialidadCreate,
    service: MedicoService = Depends(get_medico_services)
):
    created = await service.create_specialty(especializacion)
    return success_response(
        data=created.model_dump(),
        message="Especialidad creada correctamente"
    )


@router.get("/especialidades/{id}", response_model=EspecialidadDTO)
async def obtener_especializacion(id: int, service: MedicoService = Depends(get_medico_services)):
    spec = await service.get_specialty_by_id(id)
    return success_response(
        data=spec.model_dump(),
        message="Especialidad obtenida correctamente"
    )


@router.patch("/especialidades/{id}", response_model=EspecialidadDTO)
async def actualizar_especializacion(
    id: int, 
    especializacion: EspecialidadUpdate,
    service: MedicoService = Depends(get_medico_services)
):
    # Convert to dict and exclude None values for partial update
    update_data = especializacion.model_dump(exclude_none=True)
    updated = await service.update_specialty(id, update_data)
    return success_response(
        data=updated.model_dump(),
        message="Especialidad actualizada correctamente"
    )


@router.delete("/especialidades/{id}")
async def eliminar_especializacion(id: int, service: MedicoService = Depends(get_medico_services)):
    await service.delete_specialty(id)
    return success_response(
        data=None,
        message="Especialidad eliminada correctamente"
    )


@router.get("/especialidades/buscar/", response_model=list[EspecialidadDTO])
async def buscar_especializaciones(
    nombre: str = "",
    service: MedicoService = Depends(get_medico_services)
):
    specs = await service.search_specialties(nombre)
    return success_response(
        data=[s.model_dump() for s in specs],
        message="Especialidades encontradas correctamente"
    )
