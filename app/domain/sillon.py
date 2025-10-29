from dataclasses import dataclass
from typing import Optional
from app.schemas.sillon_schema import EstadoSillon, ubicacionSala


@dataclass
class Sillon:
    id_sillon: int | None
    ubicacion_sala: ubicacionSala
    estado: EstadoSillon
    observaciones: Optional[str] = None

    def cambiar_sala(self, nueva_sala: ubicacionSala) -> None:
        if self.estado == EstadoSillon.OCUPADO:
            raise ValueError("No se puede mover un sillón ocupado a otra sala.")
        self.ubicacion_sala = nueva_sala

    def esta_disponible(self) -> bool:
        return self.estado == EstadoSillon.DISPONIBLE

    def ocupar(self, motivo: Optional[str] = None) -> None:
        if self.estado != EstadoSillon.DISPONIBLE:
            raise ValueError("El sillón no está disponible para ocupar.")
        self.estado = EstadoSillon.OCUPADO
        self.observaciones = motivo

    def liberar(self) -> None:
        if self.estado != EstadoSillon.OCUPADO:
            raise ValueError("El sillón no está ocupado.")
        self.estado = EstadoSillon.DISPONIBLE
        self.observaciones = None

    def poner_en_mantenimiento(self, motivo: str) -> None:
        if self.estado == EstadoSillon.OCUPADO:
            raise ValueError("No se puede poner en mantenimiento un sillón ocupado.")
        self.estado = EstadoSillon.MANTENIMIENTO
        self.observaciones = motivo

    def inhabilitar(self, motivo: str) -> None:
        self.estado = EstadoSillon.FUERA_SERVICIO
        self.observaciones = motivo
