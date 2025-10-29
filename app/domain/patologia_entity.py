from dataclasses import dataclass
from typing import Optional

@dataclass
class Patologia:
    id_patologia: str
    nombre_patologia: str
    especialidad: Optional[str] = None
    tiempo_estimado: Optional[str] = None
    explicacion: Optional[str] = None
    tratamientos_principales: Optional[str] = None
    farmacos: Optional[str] = None
    efectos_adversos: Optional[str] = None
    gravedad: Optional[str] = None
    costo_aprox: Optional[str] = None
    evidencia: Optional[str] = None
    exito_porcentaje: Optional[str] = None
    edad_promedio: Optional[str] = None
    notas: Optional[str] = None
