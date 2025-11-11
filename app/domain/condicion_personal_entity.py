from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List



@dataclass
class CondicionPersonal:
    """
    Representa una condición médica personal (alergia, preexistencia, etc.)
    """
    id_condicion: Optional[int] = None
    codigo: Optional[str] = None
    nombre_condicion: str = ""
    tipo: str = "preexistencia"  # preexistencia | alergia | otro
    severidad: Optional[str] = None
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
