from dataclasses import dataclass
from typing import Optional


@dataclass
class TipoExamen:
    """Entidad de dominio para Tipo de Examen"""
    
    nombre: str
    id_tipo_examen: Optional[int] = None
    descripcion: Optional[str] = None
    codigo_interno: Optional[str] = None
    requiere_ayuno: bool = False
    tiempo_estimado: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del tipo de examen es obligatorio")
