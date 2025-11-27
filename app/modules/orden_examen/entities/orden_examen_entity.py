from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class OrdenExamen:
    """Entidad de dominio para Orden de Examen"""
    
    id_consulta: int
    id_paciente: int
    id_orden_examen: Optional[int] = None
    id_profesional: Optional[int] = None
    id_tipo_examen: Optional[int] = None
    id_estado: Optional[int] = None
    fecha: date = date.today()
    fecha_programada: Optional[datetime] = None
    fecha_solicitada: Optional[datetime] = None
    motivo: Optional[str] = None
    documento: Optional[str] = None
    estado: str = "pendiente"  # pendiente, en_proceso, finalizado, cancelada
    
    def __post_init__(self):
        if not self.id_consulta or self.id_consulta <= 0:
            raise ValueError("El ID de consulta médica es obligatorio")
        if not self.id_paciente or self.id_paciente <= 0:
            raise ValueError("El ID de paciente es obligatorio")
        
        estados_validos = {'pendiente', 'en_proceso', 'finalizado', 'cancelado'}
        if self.estado not in estados_validos:
            raise ValueError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
