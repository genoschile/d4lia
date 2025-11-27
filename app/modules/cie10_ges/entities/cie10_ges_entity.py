from dataclasses import dataclass
from typing import Optional


@dataclass
class Cie10Ges:
    """Entidad de dominio para la relación CIE10-GES"""
    
    id_cie10: int
    id_ges: int
    
    def __post_init__(self):
        if not self.id_cie10 or self.id_cie10 <= 0:
            raise ValueError("El ID de CIE-10 debe ser un entero positivo")
        if not self.id_ges or self.id_ges <= 0:
            raise ValueError("El ID de GES debe ser un entero positivo")
