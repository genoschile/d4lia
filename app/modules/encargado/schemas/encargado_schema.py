from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class CargoEnum(str, Enum):
    ENFERMERO = "enfermero"
    DOCTOR = "doctor"
    TECNICO = "técnico"
    ADMINISTRATIVO = "administrativo"
    OTRO = "otro"


class EncargadoBase(BaseModel):
    nombre_completo: str = Field(..., min_length=1, description="Nombre completo del encargado")
    rut: Optional[str] = Field(None, max_length=12, description="RUT del encargado")
    correo: Optional[str] = Field(None, description="Correo electrónico")
    telefono: Optional[str] = Field(None, description="Teléfono de contacto")
    cargo: CargoEnum = Field(default=CargoEnum.OTRO, description="Cargo del encargado")
    especialidad: Optional[str] = Field(None, description="Especialidad médica (si aplica)")
    activo: bool = Field(default=True, description="Estado activo/inactivo")


class EncargadoCreate(EncargadoBase):
    pass


class EncargadoUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, min_length=1)
    rut: Optional[str] = Field(None, max_length=12)
    correo: Optional[str] = None
    telefono: Optional[str] = None
    cargo: Optional[CargoEnum] = None
    especialidad: Optional[str] = None
    activo: Optional[bool] = None


class EncargadoResponse(EncargadoBase):
    id_encargado: int
    
    class Config:
        from_attributes = True
