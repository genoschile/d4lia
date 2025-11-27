from pydantic import BaseModel, Field
from typing import Optional


class MedicamentoHospitalizacionBase(BaseModel):
    id_hospitalizacion: int = Field(..., gt=0, description="ID de la hospitalización")
    id_medicamento: int = Field(..., gt=0, description="ID del medicamento")
    id_profesional: Optional[int] = Field(None, gt=0, description="ID del profesional que prescribe")
    dosis: Optional[str] = Field(None, description="Dosis prescrita")
    frecuencia: Optional[str] = Field(None, description="Frecuencia de administración")
    via_administracion: Optional[str] = Field(None, description="Vía de administración")
    duracion: Optional[str] = Field(None, description="Duración del tratamiento")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class MedicamentoHospitalizacionCreate(MedicamentoHospitalizacionBase):
    pass


class MedicamentoHospitalizacionResponse(MedicamentoHospitalizacionBase):
    class Config:
        from_attributes = True


class MedicamentoHospitalizacionDetailed(MedicamentoHospitalizacionResponse):
    nombre_medicamento: Optional[str] = None
    descripcion_medicamento: Optional[str] = None
