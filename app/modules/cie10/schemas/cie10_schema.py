from pydantic import BaseModel, Field
from typing import Optional


class Cie10Base(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=10, description="Código CIE-10 (ej: C50.1)")
    nombre: str = Field(..., min_length=1, description="Nombre de la enfermedad")
    categoria: Optional[str] = Field(None, description="Categoría o grupo")
    descripcion: Optional[str] = Field(None, description="Descripción detallada")
    activo: bool = Field(default=True, description="Estado activo/inactivo")


class Cie10Create(Cie10Base):
    pass


class Cie10Update(BaseModel):
    codigo: Optional[str] = Field(None, min_length=1, max_length=10)
    nombre: Optional[str] = Field(None, min_length=1)
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class Cie10Response(Cie10Base):
    id_cie10: int
    
    class Config:
        from_attributes = True
