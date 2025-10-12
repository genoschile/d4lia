from pydantic import BaseModel
from typing import Optional
from datetime import date


class PatologiaCreate(BaseModel):
    id_patologia: str
    nombre_patologia: str
    especialidad: Optional[str] = None


class PacienteCreate(BaseModel):
    rut: str
    nombre_completo: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    edad: Optional[int] = None
    direccion: Optional[str] = None
    antecedentes_medicos: Optional[str] = None
    id_patologia: Optional[str] = None
    fecha_inicio_tratamiento: Optional[date] = None
    observaciones: Optional[str] = None


class SillonCreate(BaseModel):
    id_sillon: str
    ubicacion_sala: str
    estado: str
    observaciones: Optional[str] = None
