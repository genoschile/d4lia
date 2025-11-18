from abc import ABC, abstractmethod
from typing import List

from app.domain.condicion_personal_entity import PacienteCondicion


class IPacienteCondicionRepository(ABC):

    # asociar condicion a paciente
    @abstractmethod
    async def asociar_a_paciente(
        self, conn, entity: PacienteCondicion
    ) -> PacienteCondicion:
        """Asocia una condición médica a un paciente."""
        ...

    @abstractmethod
    async def get_all_with_condiciones(self, conn) -> list[dict]:
        """Obtiene una lista de pacientes con sus condiciones asociadas."""
        ...

    # # listar condiciones de un paciente
    @abstractmethod
    async def listar_condicion_por_paciente(
        self, conn, id_paciente: int
    ) -> List[PacienteCondicion]:
        """Lista todas las condiciones médicas asociadas a un paciente."""
        ...

    # # obtener condicion por ids
    @abstractmethod
    async def obtener_por_ids(
        self, conn, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:
        """Obtiene una condición médica asociada a un paciente por sus IDs."""
        ...

    # actualizar condicion de un paciente
    @abstractmethod
    async def actualizar_condicion_de_paciente(
        self,
        conn,
        entity: PacienteCondicion,
    ) -> PacienteCondicion:
        """Actualiza una condición médica asociada a un paciente."""
        ...

    @abstractmethod
    async def remover_condicion(
        self, conn, id_paciente: int, id_condicion: int
    ) -> None:
        """Remueve la condición médica asociada a un paciente."""
        ...

    @abstractmethod
    async def validar_condicion(
        self, conn, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:
        """Valida una condición médica asociada a un paciente."""
        ...

    @abstractmethod
    async def invalidar_condicion(
        self, conn, id_paciente: int, id_condicion: int
    ) -> PacienteCondicion:
        """Invalida una condición médica asociada a un paciente."""
        ...

    @abstractmethod
    async def listar_condiciones_validadas(
        self, conn, id_paciente: int
    ) -> List[PacienteCondicion]:
        """Lista todas las condiciones médicas validadas asociadas a un paciente."""
        ...

    @abstractmethod
    async def listar_condiciones_no_validadas(
        self, conn, id_paciente: int
    ) -> List[PacienteCondicion]:
        """Lista todas las condiciones médicas no validadas asociadas a un paciente."""
        ...
