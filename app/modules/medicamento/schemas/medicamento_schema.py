from pydantic import BaseModel, Field
from typing import Optional


class MedicamentoBase(BaseModel):
    nombre_comercial: str = Field(..., min_length=1, description="Nombre comercial del medicamento")
    nombre_generico: Optional[str] = None
    concentracion: Optional[str] = None
    forma_farmaceutica: Optional[str] = None
    via_administracion: Optional[str] = None
    laboratorio: Optional[str] = None
    requiere_receta: bool = True
    stock_disponible: int = Field(default=0, ge=0, description="Stock disponible (no negativo)")
    observaciones: Optional[str] = None


class MedicamentoCreate(MedicamentoBase):
    pass


class MedicamentoUpdate(BaseModel):
    nombre_comercial: Optional[str] = Field(None, min_length=1)
    nombre_generico: Optional[str] = None
    concentracion: Optional[str] = None
    forma_farmaceutica: Optional[str] = None
    via_administracion: Optional[str] = None
    laboratorio: Optional[str] = None
    requiere_receta: Optional[bool] = None
    stock_disponible: Optional[int] = Field(None, ge=0)
    observaciones: Optional[str] = None


class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    
    class Config:
        from_attributes = True
