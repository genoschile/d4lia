from dataclasses import dataclass
from typing import Optional


@dataclass
class MedicamentoHospitalizacion:
    """Entidad de dominio para Medicamento en Hospitalización (n:n)"""
    
    id_hospitalizacion: int
    id_medicamento: int
    id_profesional: Optional[int] = None
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    via_administracion: Optional[str] = None
    duracion: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_hospitalizacion or self.id_hospitalizacion <= 0:
            raise ValueError("El ID de hospitalización es obligatorio")
        if not self.id_medicamento or self.id_medicamento <= 0:
            raise ValueError("El ID de medicamento es obligatorio")
