from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class TratamientoHospitalizacion:
    """Entidad de dominio para Tratamiento en Hospitalización (n:n)"""
    
    id_hospitalizacion: int
    id_tratamiento: int
    id_profesional: Optional[int] = None
    fecha_aplicacion: date = date.today()
    dosis: Optional[str] = None
    duracion: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_hospitalizacion or self.id_hospitalizacion <= 0:
            raise ValueError("El ID de hospitalización es obligatorio")
        if not self.id_tratamiento or self.id_tratamiento <= 0:
            raise ValueError("El ID de tratamiento es obligatorio")
