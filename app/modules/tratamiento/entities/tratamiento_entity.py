from dataclasses import dataclass
from typing import Optional


@dataclass
class Tratamiento:
    """Entidad de dominio para Tratamiento"""
    
    nombre_tratamiento: str
    id_tratamiento: Optional[int] = None
    descripcion: Optional[str] = None
    duracion_estimada: Optional[str] = None
    costo_aprox: Optional[str] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.nombre_tratamiento or not self.nombre_tratamiento.strip():
            raise ValueError("El nombre del tratamiento es obligatorio")
    
    def es_costoso(self, umbral: float = 1000000.0) -> bool:
        """Determina si el tratamiento es costoso según un umbral."""
        if not self.costo_aprox:
            return False
        import re
        match = re.search(r"[\d.,]+", self.costo_aprox.replace(".", "").replace(",", "."))
        if match:
            try:
                costo = float(match.group(0))
                return costo >= umbral
            except ValueError:
                return False
        return False
    
    def descripcion_resumida(self, max_chars: int = 100) -> str:
        """Devuelve un resumen del tratamiento limitado a max_chars."""
        resumen = f"{self.nombre_tratamiento}: {self.descripcion or 'Sin descripción'}"
        return resumen if len(resumen) <= max_chars else resumen[:max_chars] + "…"
