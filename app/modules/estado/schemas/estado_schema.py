from pydantic import BaseModel, Field
from typing import Optional


class EstadoBase(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del estado")
    descripcion: Optional[str] = Field(None, description="Descripción del estado")


class EstadoCreate(EstadoBase):
    pass


class EstadoResponse(EstadoBase):
    id_estado: int
    
    class Config:
        from_attributes = True
