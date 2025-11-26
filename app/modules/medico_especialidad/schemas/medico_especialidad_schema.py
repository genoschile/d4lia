# src/application/schemas.py
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class NivelEspecialidad(str, Enum):
    GENERAL = "general"
    ESPECIALISTA = "especialista"
    SUBESPECIALISTA = "subespecialista"


# --- Schemas de Especialidad ---
class EspecialidadDTO(BaseModel):
    id_especializacion: int = Field(alias="id")
    nombre: str
    nivel: str

    class Config:
        from_attributes = True
        populate_by_name = True


class EspecialidadCreate(BaseModel):
    nombre: str
    nivel: NivelEspecialidad
    codigo_fonasa: Optional[str] = ""


class EspecialidadUpdate(BaseModel):
    nombre: Optional[str] = None
    nivel: Optional[NivelEspecialidad] = None
    codigo_fonasa: Optional[str] = None


# --- Schemas de Médico ---
class MedicoBase(BaseModel):
    rut: str
    nombre: str
    apellido: str
    sexo: str
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None

    @field_validator("rut", mode="before")
    @classmethod
    def parse_rut(cls, v):
        if hasattr(v, "value"):
            return v.value
        return v


class MedicoCreate(MedicoBase):
    pass


class VinculoProfesionalDTO(BaseModel):
    """Representa la fila en consulta_profesional"""

    id_profesional: int
    especialidad: Optional[EspecialidadDTO]
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True


class MedicoResponse(MedicoBase):
    id_medico: int
    activo: bool

    especialidades: List[VinculoProfesionalDTO] = Field(
        default=[], alias="consultas_profesionales"
    )

    class Config:
        from_attributes = True
