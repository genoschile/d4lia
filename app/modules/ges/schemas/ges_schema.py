from pydantic import BaseModel, Field
from typing import Optional


class GesBase(BaseModel):
    codigo_ges: Optional[str] = Field(None, max_length=10, description="Código GES (ej: GES 18)")
    nombre: str = Field(..., min_length=1, description="Nombre del programa GES")
    descripcion: Optional[str] = Field(None, description="Descripción del programa")
    cobertura: Optional[str] = Field(None, description="Detalle de cobertura")
    dias_limite_diagnostico: Optional[int] = Field(None, gt=0, description="Días límite para diagnóstico")
    dias_limite_tratamiento: Optional[int] = Field(None, gt=0, description="Días límite para tratamiento")
    requiere_fonasa: bool = Field(default=True, description="Si requiere cobertura FONASA")
    vigente: bool = Field(default=True, description="Si el programa está vigente")


class GesCreate(GesBase):
    pass


class GesUpdate(BaseModel):
    codigo_ges: Optional[str] = Field(None, max_length=10)
    nombre: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = None
    cobertura: Optional[str] = None
    dias_limite_diagnostico: Optional[int] = Field(None, gt=0)
    dias_limite_tratamiento: Optional[int] = Field(None, gt=0)
    requiere_fonasa: Optional[bool] = None
    vigente: Optional[bool] = None


class GesResponse(GesBase):
    id_ges: int
    
    class Config:
        from_attributes = True
