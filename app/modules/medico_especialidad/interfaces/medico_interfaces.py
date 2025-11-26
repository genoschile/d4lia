from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.medico_especialidad.entities.medico_especialidad_entity import Medico, Especializacion


class IMedicoRepository(ABC):

    @abstractmethod
    async def list_all(self, conn) -> List[Medico]:
        """Lista todas medicos registrados."""
        ...

    @abstractmethod
    async def create(self, conn, medico: Medico) -> Medico:
        """Crea un nuevo médico."""
        ...

    @abstractmethod
    async def get_by_id(self, conn, id: int) -> Optional[Medico]:
        """Obtiene un médico por su ID."""
        ...

    @abstractmethod
    async def get_by_rut(self, conn, rut: str) -> Optional[Medico]:
        """Obtiene un médico por su RUT."""
        ...
        
    @abstractmethod
    async def list_active(self, conn) -> List[Medico]:
        """Lista médicos activos."""
        ...

    @abstractmethod
    async def assign_specialty(self, conn, id_medico: int, id_especialidad: int):
        """Asigna una especialidad a un médico."""
        ...
    
    @abstractmethod
    async def get_specialties_by_medico(self, conn, id_medico: int) -> List[Especializacion]:
        """Obtiene las especialidades de un médico."""
        ...
        
    @abstractmethod
    async def search_by_specialty(self, conn, especialidad_nombre: str) -> List[Medico]:
        """Busca médicos por nombre de especialidad."""
        ...


class IEspecialidadRepository(ABC):
    @abstractmethod
    async def list_all(self, conn) -> List[Especializacion]:
        ...

    @abstractmethod
    async def get_by_id(self, conn, id: int) -> Optional[Especializacion]:
        ...

    @abstractmethod
    async def create(self, conn, especialidad: Especializacion) -> Especializacion:
        ...

    @abstractmethod
    async def update(self, conn, id: int, especialidad: dict) -> Optional[Especializacion]:
        ...

    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        ...

    @abstractmethod
    async def search_by_name(self, conn, nombre: str) -> List[Especializacion]:
        ...
