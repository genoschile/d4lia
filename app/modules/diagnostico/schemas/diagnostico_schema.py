from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class TipoDiagnosticoEnum(str, Enum):
    PRESUNTIVO = "presuntivo"
    CONFIRMADO = "confirmado"
    SEGUIMIENTO = "seguimiento"


class DiagnosticoBase(BaseModel):
    id_consulta_medica: int = Field(..., gt=0, description="ID de la consulta médica")
    id_cie10: Optional[int] = Field(None, gt=0, description="ID del código CIE-10")
    id_ges: Optional[int] = Field(None, gt=0, description="ID del programa GES")
    descripcion: str = Field(..., min_length=1, description="Descripción clínica del diagnóstico")
    tipo: TipoDiagnosticoEnum = Field(default=TipoDiagnosticoEnum.PRESUNTIVO, description="Tipo de diagnóstico")
    fecha_registro: Optional[date] = None
    observaciones: Optional[str] = None


class DiagnosticoCreate(DiagnosticoBase):
    pass


class DiagnosticoUpdate(BaseModel):
    id_consulta_medica: Optional[int] = Field(None, gt=0)
    id_cie10: Optional[int] = Field(None, gt=0)
    id_ges: Optional[int] = Field(None, gt=0)
    descripcion: Optional[str] = Field(None, min_length=1)
    tipo: Optional[TipoDiagnosticoEnum] = None
    fecha_registro: Optional[date] = None
    observaciones: Optional[str] = None


class DiagnosticoResponse(DiagnosticoBase):
    id_diagnostico: int
    
    class Config:
        from_attributes = True
