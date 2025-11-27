from dataclasses import dataclass
from typing import Optional


@dataclass
class Medicamento:
    """Entidad de dominio para Medicamento"""
    
    nombre_comercial: str
    id_medicamento: Optional[int] = None
    nombre_generico: Optional[str] = None
    concentracion: Optional[str] = None
    forma_farmaceutica: Optional[str] = None
    via_administracion: Optional[str] = None
    laboratorio: Optional[str] = None
    requiere_receta: bool = True
    stock_disponible: int = 0
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.nombre_comercial or not self.nombre_comercial.strip():
            raise ValueError("El nombre comercial es obligatorio")
        if self.stock_disponible < 0:
            raise ValueError("El stock no puede ser negativo")
    
    def tiene_stock(self) -> bool:
        """Verifica si hay stock disponible"""
        return self.stock_disponible > 0
    
    def es_controlado(self) -> bool:
        """Determina si es un medicamento controlado (requiere receta)"""
        return self.requiere_receta
    
    def stock_bajo(self, umbral: int = 10) -> bool:
        """Verifica si el stock está bajo según un umbral"""
        return 0 < self.stock_disponible <= umbral
    
    def descripcion_completa(self) -> str:
        """Devuelve una descripción completa del medicamento"""
        partes = [self.nombre_comercial]
        if self.nombre_generico:
            partes.append(f"({self.nombre_generico})")
        if self.concentracion:
            partes.append(f"- {self.concentracion}")
        if self.forma_farmaceutica:
            partes.append(f"- {self.forma_farmaceutica}")
        return " ".join(partes)
