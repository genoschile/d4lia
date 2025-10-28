from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict, Any


class Encuesta(BaseModel):
    """
    Modelo de dominio para la tabla 'encuesta_sesion_json'.
    Guarda encuestas dinámicas asociadas a una sesión, con respuestas en formato JSON.
    """
    id_encuesta: Optional[int] = None
    id_sesion: int
    fecha_encuesta: Optional[date] = None
    datos: Dict[str, Any]  # JSON dinámico con todas las respuestas
    completada: Optional[bool] = True
