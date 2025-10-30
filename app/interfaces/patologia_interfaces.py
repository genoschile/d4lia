from abc import ABC, abstractmethod
from app.domain.patologia_entity import Patologia


class IPatologiaRepository(ABC):
    @abstractmethod
    async def create(self, conn, patologia: Patologia) -> Patologia: ...

    @abstractmethod
    async def get_all(self, conn) -> list[Patologia]: ...

    @abstractmethod
    async def get_by_id(self, conn, id_patologia: int) -> Patologia | None: ...

    @abstractmethod
    async def delete(self, conn, id_patologia: int) -> bool: ...

    @abstractmethod
    async def update(self, conn, id_patologia: int, data) -> bool: ...