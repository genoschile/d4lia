from pydantic import BaseModel, Field
from typing import Optional


class PatologiaTratamientoCreate(BaseModel):
    id_patologia: int = Field(..., gt=0, description="ID de la patología")
    id_tratamiento: int = Field(..., gt=0, description="ID del tratamiento")


class PatologiaTratamientoResponse(BaseModel):
    id_patologia: int
    id_tratamiento: int
    
    class Config:
        from_attributes = True


class PatologiaTratamientoDetailed(BaseModel):
    """Schema con información detallada de patología y tratamiento"""
    id_patologia: int
    id_tratamiento: int
    nombre_patologia: Optional[str] = None
    nombre_tratamiento: Optional[str] = None
    
    class Config:
        from_attributes = True
