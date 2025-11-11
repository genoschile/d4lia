from pydantic import BaseModel
from typing import Optional
from datetime import date

class CondicionPersonalBase(BaseModel):
    codigo: Optional[str] = None
    nombre_condicion: str
    tipo: Optional[str] = "preexistencia"
    severidad: Optional[str] = None
    observaciones: Optional[str] = None


class CondicionPersonalCreate(CondicionPersonalBase):
    pass


class CondicionPersonalOut(CondicionPersonalBase):
    id_condicion: int

    class Config:
        orm_mode = True


class PacienteCondicionBase(BaseModel):
    id_paciente: int
    id_condicion: int
    fecha_inicio: Optional[date] = None
    fecha_resolucion: Optional[date] = None
    validada_medico: Optional[bool] = False
    observaciones: Optional[str] = None


class PacienteCondicionOut(PacienteCondicionBase):
    condicion: CondicionPersonalOut

    class Config:
        orm_mode = True
