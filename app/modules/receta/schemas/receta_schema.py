from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class RecetaBase(BaseModel):
    id_paciente: int = Field(..., gt=0, description="ID del paciente")
    id_medico: Optional[int] = Field(None, gt=0, description="ID del médico")
    id_consulta: Optional[int] = Field(None, gt=0, description="ID de la consulta médica")
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    observaciones: Optional[str] = None
    
    @field_validator('fecha_fin')
    @classmethod
    def validar_fecha_fin(cls, v, info):
        if v and info.data.get('fecha_inicio') and v < info.data['fecha_inicio']:
            raise ValueError('La fecha de fin no puede ser anterior a la fecha de inicio')
        return v


class RecetaCreate(RecetaBase):
    pass


class RecetaUpdate(BaseModel):
    id_paciente: Optional[int] = Field(None, gt=0)
    id_medico: Optional[int] = Field(None, gt=0)
    id_consulta: Optional[int] = Field(None, gt=0)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    observaciones: Optional[str] = None


class RecetaResponse(RecetaBase):
    id_receta: int
    
    class Config:
        from_attributes = True
