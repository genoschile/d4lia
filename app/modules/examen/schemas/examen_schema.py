from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ExamenBase(BaseModel):
    id_paciente: int = Field(..., gt=0, description="ID del paciente")
    id_orden_examen: int = Field(..., gt=0, description="ID de la orden de examen")
    id_tipo_examen: Optional[int] = Field(None, gt=0, description="ID del tipo de examen")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional")
    id_instalacion: Optional[int] = Field(None, gt=0, description="ID de la instalación")
    id_estado: Optional[int] = Field(None, gt=0, description="ID del estado")
    documento: Optional[str] = Field(None, description="Ruta o referencia al documento de resultados")
    fecha: date = Field(default_factory=date.today, description="Fecha del resultado")
    resultados: Optional[str] = Field(None, description="Texto de resultados")
    resumen_resultado: Optional[str] = Field(None, description="Resumen de resultados")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class ExamenCreate(ExamenBase):
    pass


class ExamenUpdate(BaseModel):
    id_tipo_examen: Optional[int] = Field(None, gt=0)
    id_profesional: Optional[int] = Field(None, gt=0)
    id_instalacion: Optional[int] = Field(None, gt=0)
    id_estado: Optional[int] = Field(None, gt=0)
    documento: Optional[str] = None
    fecha: Optional[date] = None
    resultados: Optional[str] = None
    resumen_resultado: Optional[str] = None
    observaciones: Optional[str] = None


class ExamenResponse(ExamenBase):
    id_examen: int
    
    class Config:
        from_attributes = True
