from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime



@dataclass
class ConsultaMedica:
    """Entidad de dominio para Consulta Médica"""
    id_paciente: int
    id_consulta: Optional[int] = None
    id_profesional: Optional[int] = None
    id_estado: Optional[int] = None
    especialidad: Optional[str] = None
    fecha: date = date.today()
    fecha_programada: Optional[datetime] = None
    fecha_atencion: Optional[datetime] = None
    motivo: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_paciente:
            raise ValueError("El ID del paciente es obligatorio")
        if not self.fecha:
            raise ValueError("La fecha es obligatoria")
