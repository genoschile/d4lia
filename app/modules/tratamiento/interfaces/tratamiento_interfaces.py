from abc import ABC, abstractmethod
from typing import List, Optional


class ITratamientoRepository(ABC):
    """Interface para el repositorio de Tratamiento"""
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todos los tratamientos"""
        pass
    
    @abstractmethod
    async def get_by_id(self, conn, id: int):
        """Obtener tratamiento por ID"""
        pass
    
    @abstractmethod
    async def create(self, conn, tratamiento):
        """Crear nuevo tratamiento"""
        pass
    
    @abstractmethod
    async def update(self, conn, id: int, data: dict):
        """Actualizar tratamiento"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar tratamiento"""
        pass
    
    @abstractmethod
    async def get_by_nombre(self, conn, nombre: str):
        """Obtener tratamiento por nombre"""
        pass
