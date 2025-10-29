from typing import Optional
from pydantic import BaseModel
from datetime import date


class PacienteCreate(BaseModel):
    rut: str
    nombre_completo: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    edad: Optional[int] = None
    direccion: Optional[str] = None
    antecedentes_medicos: Optional[str] = None
    id_patologia: Optional[int] = None
    fecha_inicio_tratamiento: Optional[date] = None
    observaciones: Optional[str] = None


class PacienteResponse(BaseModel):
    id_paciente: int
    nombre_completo: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    edad: Optional[int] = None
    fecha_inicio_tratamiento: Optional[date] = None
    observaciones: Optional[str] = None
