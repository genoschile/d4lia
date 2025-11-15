from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date

from app.domain.condicion_personal_entity import (
    CondicionPersonal,
    Severidad,
    TipoCondicion,
)


class CondicionPersonalBase(BaseModel):
    codigo: Optional[str] = None
    nombre_condicion: str
    tipo: Optional[str] = "preexistencia"
    severidad: Optional[str] = None
    observaciones: Optional[str] = None


class CondicionPersonalCreate(BaseModel):
    nombre_condicion: str
    codigo: Optional[str] = None
    tipo: Optional[TipoCondicion] = TipoCondicion.preexistencia
    severidad: Optional[Severidad] = Severidad.leve
    observaciones: Optional[str] = None

    @field_validator("tipo")
    def validate_tipo(cls, v):
        if v is None:
            return None
        if v not in TipoCondicion.__members__:
            raise ValueError(f"Tipo inválido: {v}")
        return TipoCondicion[v]

    @field_validator("severidad")
    def validate_severidad(cls, v):
        if v is None:
            return None
        if v not in Severidad.__members__:
            raise ValueError(f"Severidad inválida: {v}")
        return Severidad[v]


class CondicionPersonalUpdateRequest(BaseModel):
    codigo: Optional[str] = None
    nombre_condicion: Optional[str] = None
    tipo: Optional[str] = None
    severidad: Optional[str] = None
    observaciones: Optional[str] = None


class CondicionPersonalResponse(BaseModel):
    id_condicion: Optional[int] = None
    nombre_condicion: str
    tipo: Optional[str] = None
    severidad: Optional[str] = None
    observaciones: Optional[str] = None
    codigo: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, entity: CondicionPersonal):
        return cls(
            id_condicion=entity.id_condicion,
            codigo=entity.codigo,
            nombre_condicion=entity.nombre_condicion,
            tipo=entity.tipo.value,
            severidad=entity.severidad.value if entity.severidad else None,
            observaciones=entity.observaciones,
        )


class PacienteCondicionBase(BaseModel):
    id_paciente: int
    id_condicion: int
    fecha_inicio: Optional[date] = None
    fecha_resolucion: Optional[date] = None
    validada_medico: Optional[bool] = False
    observaciones: Optional[str] = None


class AsociarCondicionPacienteRequest(BaseModel):
    id_condicion: int
    fecha_inicio: Optional[date] = None
    fecha_resolucion: Optional[date] = None
    validada_medico: Optional[bool] = False
    observaciones: Optional[str] = None


class PacienteCondicionResponse(BaseModel):
    id_paciente: int
    id_condicion: int
    fecha_inicio: Optional[date] = None
    fecha_resolucion: Optional[date] = None
    validada_medico: Optional[bool] = False
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id_paciente=entity.id_paciente,
            id_condicion=entity.id_condicion,
            fecha_inicio=entity.fecha_inicio,
            fecha_resolucion=entity.fecha_resolucion,
            validada_medico=entity.validada_medico,
            observaciones=entity.observaciones,
        )


class PacienteConCondicionesResponse(BaseModel):
    id_paciente: int
    rut: str
    nombre_completo: str  # ✔️ COINCIDE CON EL QUERY
    correo: str
    edad: int
    direccion: str | None = None
    antecedentes_medicos: str | None = None
    id_patologia: int | None = None
    fecha_inicio_tratamiento: date | None = None
    observaciones: str | None = None

    condiciones: list[PacienteCondicionResponse]

    class Config:
        from_attributes = True
