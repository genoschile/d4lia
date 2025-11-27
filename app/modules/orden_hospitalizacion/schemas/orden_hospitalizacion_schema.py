from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class EstadoOrdenHospEnum(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class OrdenHospitalizacionBase(BaseModel):
    id_paciente: int = Field(..., gt=0, description="ID del paciente")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional que ordena")
    fecha: date = Field(default_factory=date.today, description="Fecha de la orden")
    motivo: Optional[str] = Field(None, description="Motivo de la hospitalización")
    documento: Optional[str] = Field(None, description="Ruta o referencia al documento")
    estado: EstadoOrdenHospEnum = Field(default=EstadoOrdenHospEnum.PENDIENTE, description="Estado de la orden")


class OrdenHospitalizacionCreate(OrdenHospitalizacionBase):
    pass


class OrdenHospitalizacionUpdate(BaseModel):
    id_profesional: Optional[int] = Field(None, gt=0)
    fecha: Optional[date] = None
    motivo: Optional[str] = None
    documento: Optional[str] = None
    estado: Optional[EstadoOrdenHospEnum] = None


class OrdenHospitalizacionResponse(OrdenHospitalizacionBase):
    id_orden_hospitalizacion: int
    
    class Config:
        from_attributes = True
