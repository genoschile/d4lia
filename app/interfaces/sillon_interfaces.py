from abc import ABC, abstractmethod
from app.domain.sillon import Sillon


class ISillonRepository(ABC):
    
    @abstractmethod
    async def get_all(self, conn) -> list[Sillon]:
        ...