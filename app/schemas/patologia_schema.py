from pydantic import BaseModel
from typing import Optional


class PatologiaCreate(BaseModel):
    id_patologia: str | None = None
    nombre_patologia: str
    especialidad: Optional[str] = None
