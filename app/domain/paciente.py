from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Paciente:
    id_paciente: str
    nombre_completo: str
    telefono: Optional[str] = None
    edad: Optional[int] = None
    direccion: Optional[str] = None
    antecedentes_medicos: Optional[str] = None
    id_patologia: Optional[str] = None
    fecha_inicio_tratamiento: Optional[date] = None
    observaciones: Optional[str] = None

    def en_tratamiento(self, fecha_actual: date) -> bool:
        """Devuelve True si el paciente lleva menos de 6 meses desde inicio de tratamiento."""
        if not self.fecha_inicio_tratamiento:
            return False
        diff = (fecha_actual - self.fecha_inicio_tratamiento).days
        return diff <= 180
