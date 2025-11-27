from pydantic import BaseModel, Field
from typing import Optional


class TipoExamenBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del tipo de examen")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")
    codigo_interno: Optional[str] = Field(None, description="Código interno del examen")
    requiere_ayuno: bool = Field(default=False, description="Si requiere ayuno")
    tiempo_estimado: Optional[str] = Field(None, description="Tiempo estimado de realización")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")


class TipoExamenCreate(TipoExamenBase):
    pass


class TipoExamenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None
    codigo_interno: Optional[str] = None
    requiere_ayuno: Optional[bool] = None
    tiempo_estimado: Optional[str] = None
    observaciones: Optional[str] = None


class TipoExamenResponse(TipoExamenBase):
    id_tipo_examen: int
    
    class Config:
        from_attributes = True
