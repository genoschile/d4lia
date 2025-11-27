from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class TratamientoHospitalizacionBase(BaseModel):
    id_hospitalizacion: int = Field(..., gt=0, description="ID de la hospitalización")
    id_tratamiento: int = Field(..., gt=0, description="ID del tratamiento")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional que aplica")
    fecha_aplicacion: date = Field(default_factory=date.today, description="Fecha de aplicación")
    dosis: Optional[str] = Field(None, description="Dosis aplicada")
    duracion: Optional[str] = Field(None, description="Duración del tratamiento")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class TratamientoHospitalizacionCreate(TratamientoHospitalizacionBase):
    pass


class TratamientoHospitalizacionResponse(TratamientoHospitalizacionBase):
    class Config:
        from_attributes = True


class TratamientoHospitalizacionDetailed(TratamientoHospitalizacionResponse):
    nombre_tratamiento: Optional[str] = None
    descripcion_tratamiento: Optional[str] = None
