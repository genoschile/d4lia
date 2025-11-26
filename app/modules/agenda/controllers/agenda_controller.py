# app/routers/agenda.py
from fastapi import APIRouter, Query
from datetime import datetime, time, timedelta, date
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/agenda", tags=["Agenda"])


class Horario(BaseModel):
    inicio: str
    fin: str
    disponible: bool

def generar_slots(hora_inicio: time, hora_fin: time, duracion_min: int):
    slots = []
    actual = datetime.combine(date.today(), hora_inicio)
    fin = datetime.combine(date.today(), hora_fin)
    delta = timedelta(minutes=duracion_min)

    while actual + delta <= fin:
        slots.append((actual.time(), (actual + delta).time()))
        actual += delta
    return slots


@router.get("/disponibilidad", response_model=List[Horario])
def obtener_disponibilidad(
    dia: date = Query(..., description="Día a consultar"),
    duracion_min: int = 180  # 3 horas por defecto
):
    # TODO: Aquí deberías traer desde la BD las sesiones confirmadas de ese día
    sesiones_ocupadas = [
        (time(8, 0), time(11, 0)),  # ejemplo de sesión ya ocupada
    ]

    slots = generar_slots(time(8, 0), time(17, 0), duracion_min)

    horarios = []
    for inicio, fin in slots:
        # marcar como ocupado si hay intersección
        ocupado = any(
            (inicio < s_fin and fin > s_inicio) for s_inicio, s_fin in sesiones_ocupadas
        )
        horarios.append(Horario(
            inicio=inicio.strftime("%H:%M"),
            fin=fin.strftime("%H:%M"),
            disponible=not ocupado
        ))

    return horarios
