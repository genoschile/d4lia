from abc import ABC, abstractmethod
from typing import List

from app.modules.paciente_condicion.entities.condicion_personal_entity import PacienteCondicion
from app.modules.medico_especialidad.medico_especialidad_entity import Medico


class IMedicoRepository(ABC):

    @abstractmethod
    async def list_all(self, conn) -> List[Medico]:
        """Lista todas medicos registrados."""
        ...
