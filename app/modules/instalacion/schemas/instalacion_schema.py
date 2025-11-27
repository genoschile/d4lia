from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TipoInstalacionEnum(str, Enum):
    LABORATORIO = "laboratorio"
    IMAGENOLOGIA = "imagenologia"
    CLINICA = "clinica"
    EXTERNO = "externo"


class InstalacionBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre de la instalación")
    tipo: TipoInstalacionEnum = Field(default=TipoInstalacionEnum.LABORATORIO, description="Tipo de instalación")
    ubicacion: Optional[str] = Field(None, description="Dirección o ubicación")
    contacto: Optional[str] = Field(None, description="Información de contacto")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class InstalacionCreate(InstalacionBase):
    pass


class InstalacionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    tipo: Optional[TipoInstalacionEnum] = None
    ubicacion: Optional[str] = None
    contacto: Optional[str] = None
    observaciones: Optional[str] = None


class InstalacionResponse(InstalacionBase):
    id_instalacion: int
    
    class Config:
        from_attributes = True
