# app/routers/agenda.py
from fastapi import APIRouter, Query
from datetime import datetime, time, timedelta, date
from typing import List
from pydantic import BaseModel

from app.schemas.medico_especialidad_schema import MedicoResponse

router = APIRouter(prefix="/medico_especialidad", tags=["Médico y Especialidad"])


@router.post("/medicos/", response_model=MedicoResponse)
async def crear_medico():
    # Lógica para crear un médico
    pass


@router.post("/medicos/{medico_id}/especialidad/{especialidad_id}")
async def asignar_especialidad(medico_id: int, especialidad_id: int):
    # Lógica para asignar una especialidad a un médico
    pass