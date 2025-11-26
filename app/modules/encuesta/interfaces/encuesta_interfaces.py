from abc import ABC, abstractmethod
from typing import List

from app.modules.encuesta.entities.encuesta_entity import Encuesta


class IEncuestaRepository(ABC):
    @abstractmethod
    async def create(self, encuesta: Encuesta) -> Encuesta:
        """Crea una nueva encuesta en la base de datos."""
        ...
