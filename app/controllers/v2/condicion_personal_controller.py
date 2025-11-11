from fastapi import APIRouter, Depends

from app.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalOut,
    PacienteCondicionBase,
    PacienteCondicionOut,
)


router = APIRouter(prefix="/condiciones", tags=["Condiciones Personales"])


# Crear nueva condición personal
@router.post("/", response_model=CondicionPersonalOut)
def crear_condicion():
    pass


# Listar todas las condiciones registradas
@router.get("/", response_model=list[CondicionPersonalOut])
def listar_condiciones():
    pass


# Asociar una condición a un paciente
@router.post("/paciente/{id_paciente}", response_model=PacienteCondicionOut)
def asociar_condicion():
    pass
