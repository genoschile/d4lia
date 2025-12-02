from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.paciente_ges.entities.paciente_ges_entity import PacienteGes


class PacienteGesRepositoryInterface(ABC):
    """Interface para el repositorio de Paciente GES"""
    
    @abstractmethod
    async def list_all(self, conn) -> List[PacienteGes]:
        """Listar todos los registros GES de pacientes"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int) -> Optional[PacienteGes]:
        """Obtener un registro GES por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, paciente_ges: PacienteGes) -> PacienteGes:
        """Crear un nuevo registro GES para paciente"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict) -> Optional[PacienteGes]:
        """Actualizar un registro GES de paciente"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar un registro GES de paciente"""
        pass
    
    @abstractmethod
    async def get_by_paciente(self, conn, id_paciente: int) -> List[PacienteGes]:
        """Obtener todos los registros GES de un paciente"""
        pass
    
    @abstractmethod
    async def get_activos_by_paciente(self, conn, id_paciente: int) -> List[PacienteGes]:
        """Obtener registros GES activos de un paciente"""
        pass
    
    @abstractmethod
    async def get_countdown_view(self, conn, filtro_estado: Optional[str] = None):
        """Obtener datos desde la vista de countdown"""
        pass
    
    @abstractmethod
    async def get_estadisticas(self, conn) -> dict:
        """Obtener estadísticas de registros GES"""
        pass