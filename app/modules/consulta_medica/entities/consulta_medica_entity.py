from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class ConsultaMedica:
    """Entidad de dominio para Consulta Médica"""
    
    id_consulta: Optional[int]
    id_paciente: int
    id_profesional: Optional[int]
    especialidad: Optional[str]
    fecha: date
    motivo: Optional[str]
    tratamiento: Optional[str]
    observaciones: Optional[str]
    
    def __post_init__(self):
        if not self.id_paciente:
            raise ValueError("El ID del paciente es obligatorio")
        if not self.fecha:
            raise ValueError("La fecha es obligatoria")
