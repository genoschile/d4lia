from dataclasses import dataclass
from typing import Optional


@dataclass
class Cie10:
    """Entidad de dominio para CIE-10 (Clasificación Internacional de Enfermedades)"""
    
    codigo: str
    nombre: str
    id_cie10: Optional[int] = None
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    activo: bool = True
    
    def __post_init__(self):
        if not self.codigo or not self.codigo.strip():
            raise ValueError("El código CIE-10 es obligatorio")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la enfermedad es obligatorio")
