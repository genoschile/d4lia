from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Examen:
    """Entidad de dominio para Resultado de Examen"""
    
    id_paciente: int
    id_orden_examen: int
    id_examen: Optional[int] = None
    id_tipo_examen: Optional[int] = None
    id_profesional: Optional[int] = None
    id_instalacion: Optional[int] = None
    documento: Optional[str] = None
    fecha: date = date.today()
    resultados: Optional[str] = None
    resumen_resultado: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_paciente or self.id_paciente <= 0:
            raise ValueError("El ID de paciente es obligatorio")
        if not self.id_orden_examen or self.id_orden_examen <= 0:
            raise ValueError("El ID de orden de examen es obligatorio")
