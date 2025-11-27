from dataclasses import dataclass
from typing import Optional


@dataclass
class RecetaMedicamento:
    """Entidad de dominio para la relación Receta-Medicamento con detalles de prescripción"""
    
    id_receta: int
    id_medicamento: int
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    duracion: Optional[str] = None
    instrucciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_receta or self.id_receta <= 0:
            raise ValueError("El ID de receta debe ser un entero positivo")
        if not self.id_medicamento or self.id_medicamento <= 0:
            raise ValueError("El ID de medicamento debe ser un entero positivo")
    
    def tiene_instrucciones_completas(self) -> bool:
        """Verifica si tiene todos los campos de prescripción"""
        return all([self.dosis, self.frecuencia, self.duracion])
