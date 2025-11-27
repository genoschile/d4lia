from dataclasses import dataclass
from typing import Optional


@dataclass
class Ges:
    """Entidad de dominio para GES (Garantías Explícitas en Salud)"""
    
    nombre: str
    id_ges: Optional[int] = None
    codigo_ges: Optional[str] = None
    descripcion: Optional[str] = None
    cobertura: Optional[str] = None
    vigente: bool = True
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del programa GES es obligatorio")
