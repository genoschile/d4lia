from abc import ABC, abstractmethod
from app.domain.patologia import Patologia


class IPatologiaRepository(ABC):
    @abstractmethod
    async def create(self, patologia: Patologia) -> Patologia: ...

    @abstractmethod
    async def get_all(self) -> list[Patologia]: ...

    @abstractmethod
    async def update(self, patologia_id: int, patologia: Patologia) -> Patologia | None: ...

    @abstractmethod
    async def delete(self, patologia_id: int) -> bool: ...
