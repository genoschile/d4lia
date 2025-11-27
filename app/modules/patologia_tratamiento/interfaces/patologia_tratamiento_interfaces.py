from abc import ABC, abstractmethod
from typing import List


class IPatologiaTratamientoRepository(ABC):
    """Interface para el repositorio de Patología-Tratamiento"""
    
    @abstractmethod
    async def create(self, conn, patologia_tratamiento):
        """Vincular una patología con un tratamiento"""
        pass
    
    @abstractmethod
    async def delete(self, conn, id_patologia: int, id_tratamiento: int) -> bool:
        """Desvincular una patología de un tratamiento"""
        pass
    
    @abstractmethod
    async def get_tratamientos_by_patologia(self, conn, id_patologia: int) -> List:
        """Obtener todos los tratamientos de una patología"""
        pass
    
    @abstractmethod
    async def get_patologias_by_tratamiento(self, conn, id_tratamiento: int) -> List:
        """Obtener todas las patologías asociadas a un tratamiento"""
        pass
    
    @abstractmethod
    async def exists(self, conn, id_patologia: int, id_tratamiento: int) -> bool:
        """Verificar si existe la relación"""
        pass
    
    @abstractmethod
    async def list_all(self, conn) -> List:
        """Listar todas las relaciones patología-tratamiento"""
        pass
