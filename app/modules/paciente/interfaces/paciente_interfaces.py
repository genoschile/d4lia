from abc import ABC, abstractmethod
from app.modules.paciente.entities.paciente_entity import Paciente
from app.modules.sillon.entities.sillon_entity import Sillon


class IPacienteRepository(ABC):
    @abstractmethod
    async def get_all(self, conn) -> list[Paciente]: ...

    @abstractmethod
    async def create(self, conn, paciente_data) -> Paciente: ...

    @abstractmethod
    async def get_by_rut(self, conn, rut: str) -> bool: ...

    @abstractmethod
    async def get_by_id(self, conn, id_paciente: int) -> Paciente | None: ...

    @abstractmethod
    async def delete(self, conn, id_paciente: int) -> bool: ...
