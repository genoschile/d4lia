from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import date, time


class EstadoSesion(Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"


class SesionBase(BaseModel):
    id_paciente: int
    id_patologia: int | None = None
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
    fecha: date

class SesionResponse(BaseModel):
    id_sesion: int
    id_paciente: int
    fecha: date
    hora_inicio: time
    id_patologia: Optional[int] = None
    id_sillon: Optional[int] = None
    hora_fin: Optional[time] = None
    estado: EstadoSesion = EstadoSesion.PENDIENTE

