from pydantic import BaseModel, Field
from typing import Optional


class TratamientoBase(BaseModel):
    nombre_tratamiento: str = Field(..., min_length=1, description="Nombre del tratamiento")
    descripcion: Optional[str] = None
    duracion_estimada: Optional[str] = None
    costo_aprox: Optional[str] = None
    observaciones: Optional[str] = None


class TratamientoCreate(TratamientoBase):
    pass


class TratamientoUpdate(BaseModel):
    nombre_tratamiento: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None
    duracion_estimada: Optional[str] = None
    costo_aprox: Optional[str] = None
    observaciones: Optional[str] = None


class TratamientoResponse(TratamientoBase):
    id_tratamiento: int
    
    class Config:
        from_attributes = True
