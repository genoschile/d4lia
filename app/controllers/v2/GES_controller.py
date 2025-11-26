from fastapi import APIRouter, Depends

from app.modules.paciente_condicion.schemas.condicion_schema import (
    CondicionPersonalCreate,
    CondicionPersonalOut,
    PacienteCondicionBase,
    PacienteCondicionOut,
)


router = APIRouter(prefix="/GES", tags=["GES"])


# Listar GES
@router.get("/", response_model=list[CondicionPersonalOut])
def listar_ges():
    pass


# Buscar por código o nombre
@router.get("/buscar/", response_model=list[CondicionPersonalOut])
def buscar_ges(codigo: str = "", nombre: str = ""):
    pass

# Listar diagnósticos asociados a un GES
@router.get("/{id_ges}/diagnosticos", response_model=list[PacienteCondicionOut])
def listar_diagnosticos_ges(id_ges: int):
    pass