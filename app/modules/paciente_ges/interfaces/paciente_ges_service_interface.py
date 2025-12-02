from abc import ABC, abstractmethod
from typing import List, Optional
from app.modules.paciente_ges.schemas.paciente_ges_schema import (
    PacienteGesCreate,
    PacienteGesUpdate,
    PacienteGesResponse,
    PacienteGesCountdownResponse,
    PacienteGesEstadisticas
)


class PacienteGesServiceInterface(ABC):
    """Interface para el servicio de Paciente GES"""
    
    @abstractmethod
    async def list_all(self) -> List[PacienteGesResponse]:
        """Listar todos los registros GES de pacientes"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> PacienteGesResponse:
        """Obtener un registro GES por ID"""
        pass
    
    @abstractmethod
    async def create(self, data: PacienteGesCreate) -> PacienteGesResponse:
        """Crear un nuevo registro GES para paciente"""
        pass
    
    @abstractmethod
    async def update(self, id: int, data: PacienteGesUpdate) -> PacienteGesResponse:
        """Actualizar un registro GES de paciente"""
        pass
    
    @abstractmethod
    async def delete(self, id: int):
        """Eliminar un registro GES de paciente"""
        pass
    
    @abstractmethod
    async def get_by_paciente(self, id_paciente: int) -> List[PacienteGesResponse]:
        """Obtener todos los registros GES de un paciente"""
        pass
    
    @abstractmethod
    async def get_activos_by_paciente(self, id_paciente: int) -> List[PacienteGesResponse]:
        """Obtener registros GES activos de un paciente"""
        pass
    
    @abstractmethod
    async def get_countdown_view(self, filtro_estado: Optional[str] = None) -> List[PacienteGesCountdownResponse]:
        """Obtener vista de cuenta regresiva"""
        pass
    
    @abstractmethod
    async def get_estadisticas(self) -> PacienteGesEstadisticas:
        """Obtener estadísticas de registros GES"""
        pass