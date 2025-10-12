# app/schemas.py
from pydantic import BaseModel
from datetime import date, time


class SesionBase(BaseModel):
    id_paciente: str
    id_patologia: str | None = None
    id_sillon: str | None = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    tiempo_aseo_min: int
    materiales_usados: str | None = None
    estado: str


class SesionCreate(SesionBase):
    id_sesion: str


class SesionOut(SesionBase):
    id_sesion: str

    class Config:
        orm_mode = True
