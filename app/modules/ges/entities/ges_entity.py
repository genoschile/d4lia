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
    dias_limite_diagnostico: Optional[int] = None
    dias_limite_tratamiento: Optional[int] = None
    requiere_fonasa: bool = True
    vigente: bool = True
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del programa GES es obligatorio")
        if self.dias_limite_diagnostico is not None and self.dias_limite_diagnostico <= 0:
            raise ValueError("Los días límite para diagnóstico deben ser mayor a 0")
        if self.dias_limite_tratamiento is not None and self.dias_limite_tratamiento <= 0:
            raise ValueError("Los días límite para tratamiento deben ser mayor a 0")
