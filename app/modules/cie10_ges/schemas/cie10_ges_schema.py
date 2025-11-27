from pydantic import BaseModel, Field
from typing import Optional


class Cie10GesBase(BaseModel):
    id_cie10: int = Field(..., gt=0, description="ID del código CIE-10")
    id_ges: int = Field(..., gt=0, description="ID del programa GES")


class Cie10GesCreate(Cie10GesBase):
    pass


class Cie10GesResponse(Cie10GesBase):
    class Config:
        from_attributes = True


class Cie10GesDetailed(BaseModel):
    """Schema con información detallada de la relación"""
    id_cie10: int
    id_ges: int
    cie10_codigo: Optional[str] = None
    cie10_nombre: Optional[str] = None
    ges_codigo: Optional[str] = None
    ges_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True
