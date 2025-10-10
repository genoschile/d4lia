from dataclasses import dataclass
from datetime import date, time
from typing import Optional


@dataclass
class Sesion:
    id_sesion: str
    id_paciente: str
    id_patologia: Optional[str]
    id_sillon: Optional[str]
    fecha: date
    hora_inicio: time
    hora_fin: time
    tiempo_aseo_min: int
    materiales_usados: Optional[str]
    estado: str

    def duracion_total_min(self) -> int:
        """Calcula la duración total de la sesión (tratamiento + aseo)."""
        duracion = (self.hora_fin.hour * 60 + self.hora_fin.minute) - (
            self.hora_inicio.hour * 60 + self.hora_inicio.minute
        )
        return duracion + self.tiempo_aseo_min
