from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class PacienteGes:
    """Entidad de dominio para tracking de GES por paciente"""
    
    id_paciente: int
    id_ges: int
    dias_limite: int
    id_paciente_ges: Optional[int] = None
    id_diagnostico: Optional[int] = None
    fecha_activacion: date = date.today()
    fecha_vencimiento: Optional[date] = None  # calculado por trigger
    estado: str = 'activo'
    tipo_cobertura: str = 'fonasa'
    activado_por: Optional[int] = None
    fecha_completado: Optional[date] = None
    observaciones: Optional[str] = None
    
    def __post_init__(self):
        if not self.id_paciente or self.id_paciente <= 0:
            raise ValueError("El ID de paciente es obligatorio")
        if not self.id_ges or self.id_ges <= 0:
            raise ValueError("El ID de GES es obligatorio")
        if not self.dias_limite or self.dias_limite <= 0:
            raise ValueError("Los días límite deben ser mayor a 0")
        if self.estado not in ('activo', 'en_proceso', 'completado', 'vencido', 'cancelado'):
            raise ValueError(f"Estado inválido: {self.estado}")
        if self.tipo_cobertura not in ('fonasa', 'isapre', 'particular'):
            raise ValueError(f"Tipo de cobertura inválido: {self.tipo_cobertura}")
    
    # ---------------- Propiedades calculadas ----------------
    @property
    def dias_restantes(self) -> Optional[int]:
        """Calcula los días restantes hasta el vencimiento"""
        if not self.fecha_vencimiento:
            return None
        delta = self.fecha_vencimiento - date.today()
        return delta.days
    
    @property
    def prioridad(self) -> str:
        """Determina la prioridad basada en días restantes"""
        if self.estado in ('completado', 'cancelado'):
            return self.estado.capitalize()
        
        dias = self.dias_restantes
        if dias is None:
            return 'Desconocido'
        
        if dias < 0:
            return 'Vencido'
        elif dias <= 7:
            return 'Crítico'
        elif dias <= 30:
            return 'Urgente'
        else:
            return 'Normal'
    
    @property
    def porcentaje_transcurrido(self) -> Optional[float]:
        """Calcula el porcentaje de tiempo transcurrido"""
        if not self.dias_limite or self.dias_limite == 0:
            return None
        
        dias_pasados = (date.today() - self.fecha_activacion).days
        return round((dias_pasados / self.dias_limite) * 100, 2)
    
    # ---------------- Métodos de negocio ----------------
    def esta_vencido(self) -> bool:
        """Verifica si el GES está vencido"""
        if not self.fecha_vencimiento:
            return False
        return date.today() > self.fecha_vencimiento
    
    def esta_critico(self) -> bool:
        """Verifica si el GES está en estado crítico (7 días o menos)"""
        dias = self.dias_restantes
        return dias is not None and 0 <= dias <= 7
    
    def esta_urgente(self) -> bool:
        """Verifica si el GES está en estado urgente (30 días o menos)"""
        dias = self.dias_restantes
        return dias is not None and 0 <= dias <= 30
    
    def completar(self, observaciones: Optional[str] = None):
        """Marca el GES como completado"""
        self.estado = 'completado'
        self.fecha_completado = date.today()
        if observaciones:
            self.observaciones = observaciones
    
    def cancelar(self, observaciones: Optional[str] = None):
        """Cancela el GES"""
        self.estado = 'cancelado'
        if observaciones:
            self.observaciones = observaciones
