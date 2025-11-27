from abc import ABC, abstractmethod
from typing import List, Optional


class IDiagnosticoRepository(ABC):
    """Interface para el repositorio de Diagnóstico"""
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todos los diagnósticos"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int):
        """Obtener diagnóstico por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, diagnostico):
        """Crear nuevo diagnóstico"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict):
        """Actualizar diagnóstico"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar diagnóstico"""
        pass
    
    @abstractmethod
    async def get_by_consulta(self, conn, id_consulta: int) -> List:
        """Obtener diagnósticos por consulta médica"""
        pass
    
    @abstractmethod
    async def get_by_tipo(self, conn, tipo: str) -> List:
        """Obtener diagnósticos por tipo"""
        pass
    
    @abstractmethod
    async def get_con_ges(self, conn) -> List:
        """Obtener diagnósticos con cobertura GES"""
        pass
