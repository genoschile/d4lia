from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


# ----------- ENUMERATIONS -----------
class ubicacionSala(str, Enum):
    SALA_ESPERA = "sala_espera"
    CONSULTORIO_1 = "consultorio_1"
    CONSULTORIO_2 = "consultorio_2"
    CONSULTORIO_3 = "consultorio_3"
    DESCONOCIDO = "DESCONOCIDO"


class EstadoSillon(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"
    FUERA_SERVICIO = "fuera_servicio"


# ----------- RESPONSE SCHEMA -----------
class SillonResponse(BaseModel):
    id_sillon: Optional[int] = None
    ubicacion_sala: str
    estado: EstadoSillon
    observaciones: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ----------- UPDATE SCHEMA -----------
class SillonUpdate(BaseModel):
    ubicacion_sala: Optional[ubicacionSala] = None
    estado: Optional[EstadoSillon] = None
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- CREATE SCHEMA -----------
class SillonCreate(BaseModel):
    # id_sillon: Optional[int] = None
    ubicacion_sala: ubicacionSala = ubicacionSala.DESCONOCIDO
    estado: EstadoSillon
    observaciones: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "ubicacion_sala": ubicacionSala.CONSULTORIO_3.value,
                "estado": EstadoSillon.OCUPADO.value,
                "observaciones": "Sillón reservado para sesión de quimioterapia matutina.",
            }
        },
    )
