from abc import ABC, abstractmethod
from app.domain.sillon import Sillon


class ISillonRepository(ABC):

    @abstractmethod
    async def get_all(self, conn) -> list[Sillon]: ...

    @abstractmethod
    async def create_sillon(self, conn, sillon: Sillon) -> None: ...

    @abstractmethod
    async def get_by_id(self, conn, id_sillon: int) -> Sillon: ...

    @abstractmethod
    async def delete_sillon(self, conn, id_sillon: int) -> None: ...

    @abstractmethod
    async def change_state_sillon(self, conn, sillon: Sillon) -> None: ...

    @abstractmethod
    async def change_sala_sillon(self, conn, sillon: Sillon) -> None: ...
