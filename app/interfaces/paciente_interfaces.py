from abc import ABC, abstractmethod
from app.domain.paciente import Paciente
from app.domain.sillon import Sillon


class IPacienteRepository(ABC):
    @abstractmethod
    async def create(self, paciente: Paciente) -> Paciente: ...

    @abstractmethod
    async def get_all(self) -> list[Paciente]: ...

    @abstractmethod
    async def update(self, paciente_id: int, paciente: Paciente) -> Paciente | None: ...

    @abstractmethod
    async def delete(self, sillon_id: int) -> bool: ...
