from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class PacienteGesBase(BaseModel):
    id_paciente: int = Field(..., gt=0, description="ID del paciente")
    id_ges: int = Field(..., gt=0, description="ID del GES")
    dias_limite: Optional[int] = Field(None, gt=0, description="Días límite para cumplir el GES (Calculado automáticamente si se omite)")
    id_diagnostico: Optional[int] = Field(None, gt=0, description="ID del diagnóstico asociado")
    fecha_activacion: date = Field(default_factory=date.today, description="Fecha de activación del GES")
    estado: str = Field(default='activo', description="Estado del GES")
    tipo_cobertura: str = Field(default='fonasa', description="Tipo de cobertura")
    activado_por: Optional[int] = Field(None, gt=0, description="ID del médico que activó")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class PacienteGesCreate(PacienteGesBase):
    """Schema para crear un nuevo GES para paciente"""
    pass


class PacienteGesUpdate(BaseModel):
    """Schema para actualizar un GES de paciente"""
    estado: Optional[str] = Field(None, description="Nuevo estado")
    dias_limite: Optional[int] = Field(None, gt=0, description="Actualizar días límite")
    tipo_cobertura: Optional[str] = Field(None, description="Actualizar tipo de cobertura")
    fecha_completado: Optional[date] = Field(None, description="Fecha de completado")
    observaciones: Optional[str] = Field(None, description="Observaciones")


class PacienteGesResponse(PacienteGesBase):
    """Schema de respuesta con datos completos"""
    id_paciente_ges: int
    fecha_vencimiento: Optional[date]
    fecha_completado: Optional[date] = None
    
    class Config:
        from_attributes = True


class PacienteGesCountdownResponse(BaseModel):
    """Schema de respuesta con cuenta regresiva (desde la vista)"""
    id_paciente_ges: int
    id_paciente: int
    nombre_completo: str
    rut: str
    id_ges: int
    ges_nombre: str
    codigo_ges: Optional[str]
    fecha_activacion: date
    dias_limite: int
    fecha_vencimiento: Optional[date]
    estado: str
    tipo_cobertura: str
    activado_por: Optional[int]
    fecha_completado: Optional[date]
    observaciones: Optional[str]
    dias_restantes: Optional[int]
    prioridad: str
    porcentaje_transcurrido: Optional[float]
    
    class Config:
        from_attributes = True


class PacienteGesEstadisticas(BaseModel):
    """Schema para estadísticas de GES"""
    total_activos: int
    criticos: int  # <= 7 días
    urgentes: int  # <= 30 días
    vencidos: int
    completados_mes: int
    en_proceso: int
