from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Receta:
    """Entidad de dominio para Receta"""
    
    id_paciente: int
    fecha_inicio: date
    id_receta: Optional[int] = None
    id_medico: Optional[int] = None
    id_consulta: Optional[int] = None
    fecha_fin: Optional[date] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_paciente or self.id_paciente <= 0:
            raise ValueError("El ID del paciente es obligatorio y debe ser positivo")
        if not self.fecha_inicio:
            raise ValueError("La fecha de inicio es obligatoria")
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
    
    def esta_vigente(self) -> bool:
        """Verifica si la receta está vigente"""
        from datetime import date as date_class
        hoy = date_class.today()
        if self.fecha_fin:
            return self.fecha_inicio <= hoy <= self.fecha_fin
        return self.fecha_inicio <= hoy
    
    def dias_vigencia(self) -> Optional[int]:
        """Calcula los días de vigencia de la receta"""
        if self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days
        return None
