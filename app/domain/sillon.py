from dataclasses import dataclass
from typing import Optional


@dataclass
class Sillon:
    id_sillon: str
    ubicacion_sala: str
    estado: str
    observaciones: Optional[str] = None

    def esta_disponible(self) -> bool:
        return self.estado == "Disponible"

    def inhabilitar(self, motivo: str) -> None:
        self.estado = "Inhabilitado"
        self.observaciones = motivo
