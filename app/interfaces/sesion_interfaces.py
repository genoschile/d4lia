from abc import ABC, abstractmethod
from app.domain.sesion import Sesion


class ISesionRepository(ABC):
    @abstractmethod
    async def create(self, sesion: Sesion) -> Sesion: ...

    @abstractmethod
    async def get_all(self) -> list[Sesion]: ...

    @abstractmethod
    async def update(self, sesion_id: int, sesion: Sesion) -> Sesion | None: ...

    @abstractmethod
    async def delete(self, sesion_id: int) -> bool: ...
