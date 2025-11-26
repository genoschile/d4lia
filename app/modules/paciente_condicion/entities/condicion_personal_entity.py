from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class TipoCondicion(str, Enum):
    preexistencia = "preexistencia"
    alergia = "alergia"
    otro = "otro"


class Severidad(str, Enum):
    leve = "leve"
    moderada = "moderada"
    severa = "severa"
    critica = "critica"
    alta = "alta"
    variable = "variable"


@dataclass
class CondicionPersonal:
    """
    Representa una condición médica personal (alergia, preexistencia, etc.)
    """

    id_condicion: Optional[int] = None
    codigo: Optional[str] = None
    nombre_condicion: str = ""
    tipo: TipoCondicion = TipoCondicion.preexistencia
    severidad: Optional[Severidad] = None
    observaciones: Optional[str] = None


@dataclass
class PacienteCondicion:
    """
    Asociación entre un paciente y una condición médica.
    """

    id_paciente: int
    id_condicion: int
    fecha_inicio: Optional[date] = None
    fecha_resolucion: Optional[date] = None
    validada_medico: bool = False
    observaciones: Optional[str] = None

    condicion: Optional[CondicionPersonal] = None

    def __post_init__(self):
        if (
            self.fecha_resolucion
            and self.fecha_inicio
            and self.fecha_resolucion < self.fecha_inicio
        ):
            raise ValueError(
                "La fecha de resolución no puede ser anterior a la fecha de inicio"
            )

    @classmethod
    def from_update(cls, id_paciente: int, id_condicion: int, update):
        return cls(
            id_paciente=id_paciente,
            id_condicion=id_condicion,
            fecha_inicio=update.fecha_inicio,
            fecha_resolucion=update.fecha_resolucion,
            validada_medico=update.validada_medico,
            observaciones=update.observaciones,
        )

    def validar(self):
        if self.validada_medico:
            from app.core.exceptions import InvalidStateException

            raise InvalidStateException("La condición ya está validada.")

        self.validada_medico = True

    def invalidar(self):
        if not self.validada_medico:
            from app.core.exceptions import InvalidStateException

            raise InvalidStateException("La condición ya estaba sin validar.")
        self.validada_medico = False
