from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class OrdenHospitalizacion:
    """Entidad de dominio para Orden de Hospitalización"""
    
    id_paciente: int
    id_orden_hospitalizacion: Optional[int] = None
    id_profesional: Optional[int] = None
    fecha: date = date.today()
    motivo: Optional[str] = None
    documento: Optional[str] = None
    estado: str = "pendiente"  # pendiente, en_proceso, completada, cancelada
    
    def __post_init__(self):
        if not self.id_paciente or self.id_paciente <= 0:
            raise ValueError("El ID de paciente es obligatorio")
        
        estados_validos = {'pendiente', 'en_proceso', 'completada', 'cancelada'}
        if self.estado not in estados_validos:
            raise ValueError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
