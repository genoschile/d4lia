from abc import ABC, abstractmethod
from typing import List

from app.domain.encuesta import Encuesta


class IEncuestaRepository(ABC):
    @abstractmethod
    async def create(self, encuesta: Encuesta) -> Encuesta:
        """Crea una nueva encuesta en la base de datos."""
        ...

    @abstractmethod
    async def get_all(self) -> List[Encuesta]:
        """Obtiene todas las encuestas almacenadas."""
        ...
