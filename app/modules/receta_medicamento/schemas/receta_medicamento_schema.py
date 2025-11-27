from pydantic import BaseModel, Field
from typing import Optional


class RecetaMedicamentoBase(BaseModel):
    id_receta: int = Field(..., gt=0, description="ID de la receta")
    id_medicamento: int = Field(..., gt=0, description="ID del medicamento")
    dosis: Optional[str] = Field(None, description="Dosis del medicamento (ej: '500mg')")
    frecuencia: Optional[str] = Field(None, description="Frecuencia de administración (ej: 'cada 8 horas')")
    duracion: Optional[str] = Field(None, description="Duración del tratamiento (ej: '7 días')")
    instrucciones: Optional[str] = Field(None, description="Instrucciones adicionales")


class RecetaMedicamentoCreate(RecetaMedicamentoBase):
    pass


class RecetaMedicamentoUpdate(BaseModel):
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    duracion: Optional[str] = None
    instrucciones: Optional[str] = None


class RecetaMedicamentoResponse(RecetaMedicamentoBase):
    class Config:
        from_attributes = True


class RecetaMedicamentoDetailed(BaseModel):
    """Schema con información detallada del medicamento"""
    id_receta: int
    id_medicamento: int
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    duracion: Optional[str] = None
    instrucciones: Optional[str] = None
    nombre_comercial: Optional[str] = None
    nombre_generico: Optional[str] = None
    concentracion: Optional[str] = None
    forma_farmaceutica: Optional[str] = None
    
    class Config:
        from_attributes = True
