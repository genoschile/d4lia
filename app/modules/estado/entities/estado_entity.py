from dataclasses import dataclass
from typing import Optional


@dataclass
class Estado:
    """Entidad de dominio para Estado"""
    
    nombre: str
    id_estado: Optional[int] = None
    descripcion: Optional[str] = None
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del estado es obligatorio")
