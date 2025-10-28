from abc import ABC, abstractmethod
from app.domain.sillon import Sillon


class ISillonRepository(ABC):
    @abstractmethod
    async def create(self, sillon: Sillon) -> Sillon: ...

    @abstractmethod
    async def get_all(self) -> list[Sillon]: ...

    @abstractmethod
    async def update(self, sillon_id: int, sillon: Sillon) -> Sillon | None: ...

    @abstractmethod
    async def delete(self, sillon_id: int) -> bool: ...
