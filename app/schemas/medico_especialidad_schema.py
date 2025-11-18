# src/application/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Schemas de Especialidad ---
class EspecialidadDTO(BaseModel):
    id_especializacion: int
    nombre: str
    nivel: str
    
    class Config:
        from_attributes = True # Antes orm_mode

# --- Schemas de Médico ---
class MedicoBase(BaseModel):
    rut: str
    nombre: str
    apellido: str
    sexo: str
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None

class MedicoCreate(MedicoBase):
    pass

class VinculoProfesionalDTO(BaseModel):
    """Representa la fila en consulta_profesional"""
    id_profesional: int
    especialidad: Optional[EspecialidadDTO]
    fecha_registro: datetime

    class Config:
        from_attributes = True

class MedicoResponse(MedicoBase):
    id_medico: int
    activo: bool
    # Aquí anidamos las especialidades
    especialidades: List[VinculoProfesionalDTO] = Field(default=[], alias="consultas_profesionales")

    class Config:
        from_attributes = True