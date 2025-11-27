from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class OrdenExamenBase(BaseModel):
    id_paciente: int = Field(..., gt=0, description="ID del paciente")
    id_consulta: Optional[int] = Field(None, gt=0, description="ID de la consulta médica")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional que ordena")
    id_tipo_examen: Optional[int] = Field(None, gt=0, description="ID del tipo de examen")
    id_estado: Optional[int] = Field(None, gt=0, description="ID del estado")
    fecha: date = Field(default_factory=date.today, description="Fecha de la orden")
    fecha_programada: Optional[datetime] = Field(None, description="Fecha programada")
    fecha_solicitada: Optional[datetime] = Field(None, description="Fecha solicitada")
    motivo: Optional[str] = Field(None, description="Motivo del examen")
    documento: Optional[str] = Field(None, description="Ruta o referencia al documento")


class OrdenExamenCreate(OrdenExamenBase):
    pass


class OrdenExamenUpdate(BaseModel):
    id_profesional: Optional[int] = Field(None, gt=0)
    id_tipo_examen: Optional[int] = Field(None, gt=0)
    id_estado: Optional[int] = Field(None, gt=0)
    fecha: Optional[date] = None
    fecha_programada: Optional[datetime] = None
    fecha_solicitada: Optional[datetime] = None
    motivo: Optional[str] = None
    documento: Optional[str] = None


class OrdenExamenResponse(OrdenExamenBase):
    id_orden_examen: int
    
    class Config:
        from_attributes = True
