from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


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
    id_paciente: Optional[int] = Field(None, gt=0, description="ID del paciente")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional")
    id_estado: Optional[int] = Field(None, gt=0, description="ID del estado")
    especialidad: Optional[str] = Field(None, description="Especialidad de la consulta")
    fecha: Optional[date] = Field(None, description="Fecha de registro")
    fecha_programada: Optional[datetime] = Field(None, description="Fecha programada")
    fecha_atencion: Optional[datetime] = Field(None, description="Fecha real de atención")
    motivo: Optional[str] = Field(None, description="Motivo de la consulta")
    tratamiento: Optional[str] = Field(None, description="Tratamiento aplicado")
    observaciones: Optional[str] = None


class ConsultaMedicaResponse(ConsultaMedicaBase):
    id_consulta: int

    class Config:
        from_attributes = True
