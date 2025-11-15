from abc import ABC, abstractmethod
from typing import List


class IPacienteCondicionRepository(ABC):

    # asociar condicion a paciente
    @abstractmethod
    async def asociar_a_paciente(self, id_paciente: int, id_condicion: int) -> None:
        """Asocia una condición médica a un paciente."""
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
