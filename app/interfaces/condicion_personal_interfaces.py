from abc import ABC, abstractmethod
from typing import List

from app.modules.paciente_condicion.entities.condicion_personal_entity import CondicionPersonal


class ICondicionPersonalRepository(ABC):
    @abstractmethod
    async def create(
        self, conn, condicion_personal: CondicionPersonal
    ) -> CondicionPersonal:
        """Crea una nueva encuesta en la base de datos."""
        ...

    @abstractmethod
    async def exists_by_name(self, conn, nombre_condicion: str) -> bool:
        """Verifica si una condición médica existe por su nombre."""
        ...

    # obtener una condicion por id
    @abstractmethod
    async def get_by_id(self, conn, id_condicion: int) -> CondicionPersonal:
        """Obtiene una condición médica por su ID."""
        ...

    # actualizar una condicion existente
    @abstractmethod
    async def update(self, conn, id_condicion: int, data: dict) -> CondicionPersonal | None:
        """Actualiza una condición médica existente."""
        ...

    # eliminar una condicion por id
    @abstractmethod
    async def delete(self, conn, id_condicion: int) -> bool:
        """Elimina una condición médica por su ID."""
        ...

    # buscar por codigo o nombre
    @abstractmethod
    async def search(
        self, conn, codigo: str = "", nombre: str = ""
    ) -> List[CondicionPersonal]:
        """Busca condiciones médicas por código o nombre."""
        ...

    # # asociar condicion a paciente
    # @abstractmethod
    # async def asociar_a_paciente(self, id_paciente: int, id_condicion: int) -> None:
    #     """Asocia una condición médica a un paciente."""
    #     ...

    # listar condiciones registradas
    @abstractmethod
    async def list_all(self, conn) -> List[CondicionPersonal]:
        """Lista todas las condiciones médicas registradas."""
        ...

    # # listar condiciones de un paciente
    # @abstractmethod
    # async def list_by_paciente(self, id_paciente: int) -> List[CondicionPersonal]:
    #     """Lista todas las condiciones médicas asociadas a un paciente."""
    #     ...

    # # obtener detalles de la condicion de un paciente
    # @abstractmethod
    # async def get_paciente_condicion(
    #     self, id_paciente: int, id_condicion: int
    # ) -> CondicionPersonal:
    #     """Obtiene los detalles de una condición médica asociada a un paciente."""
    #     ...

    # # actualizar la condicion de un paciente
    # @abstractmethod
    # async def update_paciente_condicion(
    #     self, id_paciente: int, id_condicion: int, fecha_resolucion: str
    # ) -> None:
    #     """Actualiza la condición médica asociada a un paciente."""
    #     ...

    # # remover la condicion de un paciente
    # @abstractmethod
    # async def remove_paciente_condicion(
    #     self, id_paciente: int, id_condicion: int
    # ) -> None:
    #     """Remueve la condición médica asociada a un paciente."""
    #     ...

    # # validar condicion de un paciente por medico
    # @abstractmethod
    # async def validar_condicion_medico(
    #     self, id_paciente: int, id_condicion: int
    # ) -> None:
    #     """Valida la condición médica de un paciente por un médico."""
    #     ...
