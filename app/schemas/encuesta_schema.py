from pydantic import BaseModel
from enum import Enum


class TipoEncuesta(str, Enum):
    pre_sesion = "pre_sesion"
    satisfaccion = "satisfaccion"
    seguimiento = "seguimiento"
    confirmacion = "confirmacion"
    evaluacion_medica = "evaluacion_medica"

    # trigger o al evento sesion


class GenerarLinkSchema(BaseModel):
    paciente_id: int
    sesion_id: int
    tipo_encuesta: TipoEncuesta


class EncuestaCreate(BaseModel):
    id_sesion: int
    tipo_encuesta: TipoEncuesta
    datos: dict
