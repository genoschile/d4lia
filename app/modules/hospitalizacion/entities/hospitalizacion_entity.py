from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Hospitalizacion:
    """Entidad de dominio para Hospitalización"""
    
    id_orden_hospitalizacion: int
    id_paciente: int
    id_hospitalizacion: Optional[int] = None
    id_profesional: Optional[int] = None
    fecha_ingreso: date = date.today()
    fecha_alta: Optional[date] = None
    habitacion: Optional[str] = None
    observacion: Optional[str] = None
    estado: str = "activa"  # activa, alta, cancelada
    
    def __post_init__(self):
        if not self.id_orden_hospitalizacion or self.id_orden_hospitalizacion <= 0:
            raise ValueError("El ID de orden de hospitalización es obligatorio")
        if not self.id_paciente or self.id_paciente <= 0:
            raise ValueError("El ID de paciente es obligatorio")
        
        estados_validos = {'activa', 'alta', 'cancelada'}
        if self.estado not in estados_validos:
            raise ValueError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
