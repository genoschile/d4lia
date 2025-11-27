from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class Sesion:
    id_paciente: int
    fecha: date
    hora_inicio: str
    id_sesion: int | None = None
    id_patologia: Optional[int] = None
    id_tratamiento: Optional[int] = None
    id_sillon: Optional[int] = None
    hora_fin: Optional[str] = None
    tiempo_aseo_min: Optional[int] = None
    materiales_usados: Optional[str] = None
    estado: str = "Pendiente"


