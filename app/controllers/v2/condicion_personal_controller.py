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


# Obtener una condición por ID
@router.get("/{id}", response_model=CondicionPersonalOut)
def obtener_condicion(id: int):
    pass


# Actualizar una condición existente
@router.put("/{id}", response_model=CondicionPersonalOut)
def actualizar_condicion(id: int):
    pass


# Eliminar una condición por ID
@router.delete("/{id}", response_model=dict)
def eliminar_condicion(id: int):
    pass


# Buscar por código o nombre
@router.get("/buscar/", response_model=list[CondicionPersonalOut])
def buscar_condiciones(codigo: str = "", nombre: str = ""):
    pass


# Asociar una condición a un paciente
@router.post("/paciente/{id_paciente}", response_model=PacienteCondicionOut)
def asociar_condicion(id_paciente: int, condicion: PacienteCondicionBase):
    pass


# Listar todas las condiciones registradas
@router.get("/", response_model=list[CondicionPersonalOut])
def listar_condiciones():
    pass


# Listar condiciones de un paciente
@router.get("/paciente/{id_paciente}", response_model=list[PacienteCondicionOut])
def listar_condiciones_paciente(id_paciente: int):
    pass


# Obtener detalle de una condición específica del paciente
@router.get(
    "/paciente/{id_paciente}/condicion/{id_condicion}",
    response_model=PacienteCondicionOut,
)
def obtener_detalle_condicion_paciente(id_paciente: int, id_condicion: int):
    pass


# Actualizar la condición del paciente
@router.put(
    "/paciente/{id_paciente}/condicion/{id_condicion}",
    response_model=PacienteCondicionOut,
)
def actualizar_condicion_paciente(id_paciente: int, id_condicion: int):
    pass


# Remover una condición del paciente
@router.delete("/paciente/{id_paciente}/condicion/{id_condicion}", response_model=dict)
def remover_condicion_paciente(id_paciente: int, id_condicion: int):
    pass


# Validar una condición por un médico
@router.post(
    "/paciente/{id_paciente}/condicion/{id_condicion}/validar",
    response_model=PacienteCondicionOut,
)
def validar_condicion_paciente(id_paciente: int, id_condicion: int):
    pass
