from abc import ABC, abstractmethod
from typing import List, Optional


class IRecetaRepository(ABC):
    """Interface para el repositorio de Receta"""
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todas las recetas"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int):
        """Obtener receta por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, receta):
        """Crear nueva receta"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict):
        """Actualizar receta"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar receta"""
        pass
    
    @abstractmethod
    async def get_by_paciente(self, conn, id_paciente: int) -> List:
        """Obtener recetas por paciente"""
        pass
    
    @abstractmethod
    async def get_by_medico(self, conn, id_medico: int) -> List:
        """Obtener recetas por médico"""
        pass
    
    @abstractmethod
    async def get_by_consulta(self, conn, id_consulta: int) -> List:
        """Obtener recetas por consulta médica"""
        pass
