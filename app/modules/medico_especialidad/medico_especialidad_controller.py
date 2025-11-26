from fastapi import APIRouter, Depends, Query
from app.core.exceptions import NotImplementedException
from app.core.instance import get_medico_services
from app.helpers.response import error_response, success_response
from app.modules.medico_especialidad.medico_especialidad_schema import MedicoResponse
from app.modules.medico_especialidad.medico_service import MedicoService

router = APIRouter(prefix="/medico_especialidad", tags=["Médico y Especialidad"])


@router.post("/medicos/", response_model=MedicoResponse)
async def crear_medico():
    # Lógica para crear un médico
    raise NotImplementedException("Funcionalidad no implementada aún")


# Listar médicos
@router.get("/medicos", response_model=list[MedicoResponse])
async def listar_medicos(medico_service: MedicoService = Depends(get_medico_services)):

    medicos = await medico_service.listar_medicos()

    return success_response(data=medicos, message="Médicos listados correctamente")


@router.post("/medicos/{medico_id}/especialidad/{especialidad_id}")
async def asignar_especialidad(medico_id: int, especialidad_id: int):
    # Lógica para asignar una especialidad a un médico
    raise NotImplementedException("Funcionalidad no implementada aún")


# Listar todas las especializaciones médicas
@router.get("/", response_model=list)
async def listar_especializaciones():
    raise NotImplementedException("Funcionalidad no implementada aún")


# Crear una nueva especialización médica
@router.post("/", response_model=dict)
async def crear_especializacion(especializacion: dict):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Actualizar una especialización médica existente
@router.put("/{id}", response_model=dict)
async def actualizar_especializacion(id: int, especializacion: dict):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Eliminar una especialización médica
@router.delete("/{id}", response_model=dict)
async def eliminar_especializacion(id: int):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Obtener una especialización médica por ID
@router.get("/{id}", response_model=dict)
async def obtener_especializacion(id: int):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Buscar especializaciones médicas por nombre
@router.get("/buscar/", response_model=list)
async def buscar_especializaciones(nombre: str = ""):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Listar especializaciones médicas de un médico
@router.get("/medico/{id_medico}", response_model=list)
async def listar_especializaciones_medico(id_medico: int):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Asignar especialización a un médico
@router.post("/medico/{id_medico}", response_model=dict)
async def asignar_especializacion_medico(id_medico: int, especializacion: dict):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Obtener médico por ID
@router.get("/{id}", response_model=dict)
async def obtener_medico(id: int):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Buscar médicos por especialidad
@router.get("/buscar/", response_model=list)
async def buscar_medicos(especialidad: str):
    raise NotImplementedException("Funcionalidad no implementada aún")


# Listar especialidades médicas
@router.get("/especialidades/", response_model=list)
async def listar_especialidades():
    raise NotImplementedException("Funcionalidad no implementada aún")


# Listar médicos activos
@router.get("/activos/", response_model=list)
async def listar_medicos_activos():
    raise NotImplementedError("Funcionalidad no implementada aún")


# Obtener el perfil del médico que atendió a un paciente
@router.get("/perfil/paciente/{id_paciente}", response_model=dict)
async def obtener_perfil_medico_paciente(id_paciente: int):
    raise NotImplementedError("Funcionalidad no implementada aún")
