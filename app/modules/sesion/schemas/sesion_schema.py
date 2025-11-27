import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import time, datetime, date


class EstadoSesion(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"


class SesionBase(BaseModel):
    id_paciente: int
    id_patologia: int | None = None
    id_tratamiento: int | None = None
    id_sillon: int | None = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    tiempo_aseo_min: int
    materiales_usados: str | None = None
    estado: EstadoSesion = EstadoSesion.PENDIENTE



class SesionCreate(BaseModel):
    id_paciente: int
    id_sillon: int
    id_patologia: Optional[int] = None
    id_tratamiento: Optional[int] = None
    hora_inicio: time
    fecha: date
    estado: EstadoSesion = EstadoSesion.PENDIENTE

    @field_validator("hora_inicio", mode="before")
    def parse_hora_inicio(cls, v):
        # Si viene en formato "2025-10-30T09:30", lo convertimos
        if isinstance(v, str) and "T" in v:
            return datetime.fromisoformat(v).time()
        return v


class SesionResponse(BaseModel):
    id_sesion: int
    id_paciente: int
    fecha: date
    hora_inicio: time
    id_patologia: Optional[int] = None
    id_tratamiento: Optional[int] = None
    id_sillon: Optional[int] = None
    hora_fin: Optional[time] = None
    estado: EstadoSesion = EstadoSesion.PENDIENTE


