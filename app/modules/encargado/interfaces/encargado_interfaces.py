from abc import ABC, abstractmethod
from typing import List, Optional


class IEncargadoRepository(ABC):
    """Interface para el repositorio de Encargado"""
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todos los encargados"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int):
        """Obtener encargado por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, encargado):
        """Crear nuevo encargado"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict):
        """Actualizar encargado"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar encargado"""
        pass
    
    @abstractmethod
    async def get_by_rut(self, conn, rut: str):
        """Obtener encargado por RUT"""
        pass
    
    @abstractmethod
    async def get_by_cargo(self, conn, cargo: str) -> List:
        """Obtener encargados por cargo"""
        pass
    
    @abstractmethod
    async def get_activos(self, conn) -> List:
        """Obtener encargados activos"""
        pass
