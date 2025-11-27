from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Diagnostico:
    """Entidad de dominio para Diagnóstico médico"""
    
    id_consulta_medica: int
    descripcion: str
    id_diagnostico: Optional[int] = None
    id_cie10: Optional[int] = None
    id_ges: Optional[int] = None
    tipo: str = "presuntivo"  # presuntivo, confirmado, seguimiento
    fecha_registro: Optional[date] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_consulta_medica or self.id_consulta_medica <= 0:
            raise ValueError("El ID de consulta médica es obligatorio y debe ser positivo")
        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripción del diagnóstico es obligatoria")
        
        tipos_validos = {'presuntivo', 'confirmado', 'seguimiento'}
        if self.tipo not in tipos_validos:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(tipos_validos)}")
    
    def es_confirmado(self) -> bool:
        """Verifica si el diagnóstico está confirmado"""
        return self.tipo == "confirmado"
    
    def tiene_cobertura_ges(self) -> bool:
        """Verifica si tiene cobertura GES"""
        return self.id_ges is not None
    
    def tiene_codigo_cie10(self) -> bool:
        """Verifica si tiene código CIE-10"""
        return self.id_cie10 is not None
