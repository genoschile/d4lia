from dataclasses import dataclass


@dataclass
class PatologiaTratamiento:
    """Entidad de dominio para la relación Patología-Tratamiento"""
    
    id_patologia: int
    id_tratamiento: int
    
    def __post_init__(self):
        if not self.id_patologia or self.id_patologia <= 0:
            raise ValueError("El ID de patología debe ser un entero positivo")
        if not self.id_tratamiento or self.id_tratamiento <= 0:
            raise ValueError("El ID de tratamiento debe ser un entero positivo")
