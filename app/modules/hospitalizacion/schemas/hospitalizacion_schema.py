from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class EstadoHospitalizacionEnum(str, Enum):
    ACTIVA = "activa"
    ALTA = "alta"
    CANCELADA = "cancelada"


class HospitalizacionBase(BaseModel):
    id_orden_hospitalizacion: int = Field(..., gt=0, description="ID de la orden de hospitalización")
    id_paciente: int = Field(..., gt=0, description="ID del paciente")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional responsable")
    fecha_ingreso: date = Field(default_factory=date.today, description="Fecha de ingreso")
    fecha_alta: Optional[date] = Field(None, description="Fecha de alta")
    habitacion: Optional[str] = Field(None, description="Habitación o cama asignada")
    observacion: Optional[str] = Field(None, description="Observaciones generales")
    estado: EstadoHospitalizacionEnum = Field(default=EstadoHospitalizacionEnum.ACTIVA, description="Estado de la hospitalización")


class HospitalizacionCreate(HospitalizacionBase):
    pass


class HospitalizacionUpdate(BaseModel):
    id_profesional: Optional[int] = Field(None, gt=0)
    fecha_ingreso: Optional[date] = None
    fecha_alta: Optional[date] = None
    habitacion: Optional[str] = None
    observacion: Optional[str] = None
    estado: Optional[EstadoHospitalizacionEnum] = None


class HospitalizacionResponse(HospitalizacionBase):
    id_hospitalizacion: int
    
    class Config:
        from_attributes = True
