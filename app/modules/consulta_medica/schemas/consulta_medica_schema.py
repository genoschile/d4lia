from pydantic import BaseModel
from typing import Optional
from datetime import date


class ConsultaMedicaBase(BaseModel):
    id_paciente: int
    id_profesional: Optional[int] = None
    especialidad: Optional[str] = None
    fecha: date
    motivo: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None


class ConsultaMedicaCreate(ConsultaMedicaBase):
    pass


class ConsultaMedicaUpdate(BaseModel):
    id_paciente: Optional[int] = None
    id_profesional: Optional[int] = None
    especialidad: Optional[str] = None
    fecha: Optional[date] = None
    motivo: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None


class ConsultaMedicaResponse(ConsultaMedicaBase):
    id_consulta: int

    class Config:
        from_attributes = True
